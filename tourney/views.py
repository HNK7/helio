from django.conf import settings
from django.db import connections, transaction
from django.db.models import F, Count, Q
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from tourney.models import *
from tourney.forms import *
import gdrive
import brother
from twilio.rest import TwilioRestClient
from phonenumbers import parse, format_number, PhoneNumberFormat
from string import Template
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.decorators import login_required
from tourney.phoenixcard import PhoenixCard

def convert_to_e164(raw_phone):
    if not raw_phone:
        return

    if raw_phone[0] == '+':
        # Phone number may already be in E.164 format.
        parse_type = None
    else:
        # If no country code information present, assume it's a US number
        parse_type = "US"

    phone_representation = parse(raw_phone, parse_type)
    return format_number(phone_representation, PhoneNumberFormat.E164)


def send_sms(to_phone, msg):
    if settings.SMS['LIVE']:
        client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.sms.messages.create(to=convert_to_e164(to_phone), from_="+12622932782", body=msg)


def send_draw_sms(request, e_id):
    event = get_object_or_404(Event, id=e_id)
    teams = Team.objects.filter(event=event)
    if event.draw != 'L' or teams.count() < 4 or event.draw_sms_sent():
        return HttpResponseRedirect(reverse('22k:event_signup', args=(event.id,)))

    for team in teams:

        players = team.players.all()
        for i in range(0, len(players)):
            player = players[i]
            partner = players[i+1] if i == 0 else players[i-1]
            stat_rank = partner.stat_rank(event.tournament)
            partner_stat = '%s, %s' % (stat_rank['MPR'], stat_rank['PPD'])
            sms_msg = Template(settings.SMS_MSG['DRAW'])
            sms_msg = sms_msg.safe_substitute(name=player.full_name,
                                              event_title=event.title,
                                              partner=partner.full_name,
                                              stat=partner_stat)
            try:
                send_sms(player.phone, sms_msg)
            except:
                pass

    SMSLog.objects.create(event=event, category='DRAW')
    return HttpResponseRedirect(reverse('22k:event_signup', args=(event.id,)))


# @login_required
def index(request):
    tournament_list = Tournament.objects.all().order_by('-start_at').annotate(num_players=Count('players'))
    context = {'tournament_list': tournament_list}
    if not request.session.get('tournament_id'):
        request.session['tournament_id'] = tournament_list[0].id
        request.session['tournament_title'] = tournament_list[0].title
        return HttpResponseRedirect(reverse('22k:index'))
    else:
        return render(request, 'tourney/index.html', context)


def tourney_dashboard(request, t_id):
    context = dict()
    tournament = get_object_or_404(Tournament, pk=t_id)
    if request.session.get('tournament_id') != t_id:
        request.session['tournament_id'] = t_id
        request.session['tournament_title'] = tournament.title


    # context['events'] = tournament.event_set.all().order_by('start_at').annotate(num_signups=Count('team'))
    context['events'] = tournament.event_set.all().order_by('start_at')
    context['tournament'] = tournament
    return render(request, 'tourney/tourney_dashboard.html', context)


def tourney_create(request):
    context = dict()
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/22k')
    else:
        form = TournamentForm()
    context['form'] = form
    return render(request, 'tourney/tourney_create.html', context)


def event_create(request, t_id):
    context = dict()
    tournament = get_object_or_404(Tournament, id=t_id)

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('22k:tourney_dashboard', args=(t_id,)))
    else:
        form = EventForm(initial={'tournament': t_id})
    context['form'] = form
    context['tournament'] = tournament
    return render(request, 'tourney/event_create.html', context)


def event_edit(request, e_id):
    context = dict()
    event = get_object_or_404(Event, id=e_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('22k:tourney_dashboard', args=(event.tournament.id,)))
    else:
        form = EventForm(instance=event)
    context['tournament'] = event.tournament
    context['event'] = event
    context['form'] = form
    return render(request, 'tourney/event_edit.html', context)


def player(request):
    context = dict()
    context['tournament_list'] = Tournament.objects.all()

    players = Player.objects.all()
    context['players'] = players
    context['player_total'] = len(players)
    return render(request, 'tourney/player.html', context)


def _do_card_copy(old_cardno, old_rfid, new_cardno, new_rfid):
    cursor = connections['hi'].cursor()
    cursor.execute("UPDATE checkrfid set utime=now() where rfid=%s", [new_rfid])
    cursor.execute("INSERT INTO cardcopy values(%s, %s, %s, %s, now())", [old_rfid, old_cardno, new_rfid, new_cardno])
    cursor.execute("UPDATE checkrfid set dtime=now() where rfid=%s", [old_rfid])
    cursor.execute('UPDATE userinfo SET cardno=%s where cardno=%s', [new_cardno, old_cardno])
    transaction.commit_unless_managed(using='hi')

    # update card info in helio
    Card.objects.filter(rfid=old_rfid).update(rfid=new_rfid, cardno=new_cardno)


def card_copy(request, e_id):
    context = dict()
    entry = get_object_or_404(Entry, id=e_id)
    if request.method == 'POST':
        form = CardCopyForm(request.POST)
        if form.is_valid():
            new_rfid = form.cleaned_data['new_card']
            current_cardno = form.cleaned_data['current_card']
            current_rfid = form.cleaned_data['current_rfid']

            current_card = PhoenixCard(cardno=current_cardno)
            new_card = PhoenixCard(rfid=new_rfid)

            # make sure new card number is valid
            try:
                new_card_number = new_card.get_cardno()
            except Exception:
                messages.error(request, 'Invalid card number!')
                return HttpResponseRedirect(reverse('22k:card_copy', args=(entry.id,)))
            # check if it's new one
            if not new_card.is_new():
                messages.error(request, 'Card is already in use! Try with new one')
                return HttpResponseRedirect(reverse('22k:card_copy', args=(entry.id,)))
            # make card coopy
            _do_card_copy(current_cardno, current_rfid, new_card_number, new_rfid)


            return HttpResponseRedirect(reverse('22k:entry_detail', args=(entry.tournament.id, entry.id)))
    else:
        current_card = {'current_card': entry.player.card.cardno,
                        'current_rfid': entry.player.card.rfid}
        form = CardCopyForm(initial=current_card)

    context['form'] = form
    context['entry'] = entry
    return render(request, 'tourney/card_copy.html', context)



def entry(request, t_id):
    context = dict()
    context['tournament_list'] = Tournament.objects.all()
    tourney = get_object_or_404(Tournament, pk=t_id)
    context['tournament'] = tourney

    entry = Entry.objects.filter(tournament=tourney).order_by('-created_at')
    # entry = Entry.objects.filter(tournament=tourney).order_by('-created_at').select_related('player', 'player__card')

    context['entry'] = entry
    return render(request, 'tourney/entry.html', context)

def entry_detail(request, t_id, e_id):
    context = dict()
    entry = get_object_or_404(Entry, pk=e_id)
    event_list = []
    event_list += [ de.event for de in entry.player.drawentry_set.filter(event__tournament=entry.tournament) ]
    event_list += [ t.event for t in entry.player.team_set.filter(event__tournament=entry.tournament) ]

    paid_events = SignupPayment.objects.filter(player=entry.player, event__tournament=entry.tournament, paid=True)
    context['signup_payment'] = paid_events
    context['entry'] = entry
    context['player'] = entry.player
    context['signup_events'] = event_list
    context['entry_history'] = entry.player.entry_set.all().order_by('-created_at')

    # raise Exception('debug')
    return render(request, 'tourney/entry_detail.html', context)


def entry_edit(request, t_id, e_id):
    context = dict()
    context['tournament'] = Tournament.objects.get(pk=t_id)
    entry = get_object_or_404(Entry, id=e_id)

    if request.method == 'POST':
        form = EntryForm(request.POST) # bound form with POST data

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            mobile = form.cleaned_data['mobile']
            balance_membership = form.cleaned_data['balance_membership']
            balance_signup = form.cleaned_data['balance_signup']
            balance_card = form.cleaned_data['balance_card']
            qualified = form.cleaned_data['qualified']

            player = entry.player
            if first_name != player.first_name or last_name != player.last_name:
                player.first_name = first_name
                player.last_name = last_name
                # update nick name on player's card
                update_temp_card(player.full_name, player.card.rfid)

            player.gender = gender
            player.phone = mobile
            player.save()

            entry.balance_membership = balance_membership
            entry.balance_signup = balance_signup
            entry.balance_card = balance_card
            entry.qualified = qualified
            entry.save()

            # update team and player stat
            # update_stat(form.cleaned_data['mpr_event'], form.cleaned_data['ppd_event'], entry.player.rfid)
            return HttpResponseRedirect(reverse('22k:entry', args=(t_id,)))

    else:
        player = entry.player
        entry_data = {'first_name': player.first_name.title(),
                      'last_name': player.last_name.title(),
                      'gender': player.gender,
                      'mobile': player.phone,
                      'balance_membership': entry.balance_membership,
                      'balance_signup': entry.balance_signup,
                      'balance_card': entry.balance_card,
                      'qualified': entry.qualified}
        form = EntryForm(initial=entry_data)

    context['form'] = form
    context['entry'] = entry
    return render(request, 'tourney/entry_edit.html', context)


def entry_big(request, t_id):
    context = dict()
    context['tournament_list'] = Tournament.objects.all()
    tourney = get_object_or_404(Tournament, pk=t_id)
    context['tournament'] = tourney

    entry = Entry.objects.filter(tournament=tourney)
    context['entry'] = entry
    return render(request, 'tourney/entry_big.html', context)


def profile(request, p_id):
    context = dict()
    # context['tournament_list'] = Tournament.objects.all()
    player = get_object_or_404(Player, id=p_id)
    casual_stat = player.casual_stat()
    event_stat = player.event_stat()
    # entries = player.entry_set.all()

    context['player'] = player
    # context['entries'] = entries
    context['casual_stat'] = casual_stat
    context['event_stat'] = event_stat
    return render(request, 'tourney/profile.html', context)


def profile_edit(request, p_id):
    context = dict()
    context['tournament_list'] = Tournament.objects.all()
    player = get_object_or_404(Player, id=p_id)
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('22k:profile', args=(p_id,)))

    else:
        form = EntryForm(instance=player)
    context['form'] = form
    context['player'] = player
    return render(request, 'tourney/profile_edit.html', context)


def _get_member(rfid):
    return Player.objects.filter(rfid=rfid)


def _userinfo(rfid):
    cursor = connections['hi'].cursor()
    cursor.execute("""SELECT b.rfid, %s, name, cardno, realname, m_sex, m_email, m_phone, m_id
                FROM userinfo a
                join  members b on a.rfid=b.rfid
                where b.rfid = getorigrfid2(%s)""", (rfid, rfid))
    r = cursor.fetchone()
    return {'org_rfid': r[0], 'card_rfid': int(r[1]),
            'screen_name': r[2], 'cardno': r[3], 'real_name': r[4], 'gender': r[5],
            'email': r[6], 'phone': r[7], 'id': r[8]}


def _original_rfid(rfid):
    cursor = connections['hi'].cursor()
    cursor.execute("SELECT getorigrfid2(%s)", [rfid, ])
    r = cursor.fetchone()
    return r


def _is_new_card(rfid):
    cursor = connections['hi'].cursor()
    cursor.execute("SELECT FROM userinfo%s", [rfid, ])
    r = cursor.fetchone()
    return r


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    "Returns a rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchone()
    ]


def _card_number(rfid):
    cursor = connections['hi'].cursor()
    cursor.execute("SELECT cardno FROM checkrfid where rfid=%s", [rfid])
    r = cursor.fetchone()
    return r[0]


def _card_info(rfid):
    """Get card info.
    There are 5 different card types:
    1. blank/never used new one
        no userinfo (name is null), no members(m_num is null)  and utime is null
    2. used on console but not registered on the web
        userinfo record but no members(m_num is null) and utime is still null
    3. registered as a principal card

    4. registered as an extra card

    5. copied card

    """
    cursor = connections['hi'].cursor()
    cursor.execute("""SELECT %s, (select cardno from checkrfid where rfid=%s),
                        a.cardno, a.rfid, b.rfid, c.rfid, name, m_num, utime,
                        realname, m_sex, m_email, m_phone, m_id, m_zip, ppd_ta2, mpr_ta2
                        FROM checkrfid a
                        LEFT JOIN userinfo b on a.rfid=b.rfid
                        LEFT JOIN members c on b.m_num=c.num
                        LEFT JOIN useravg d on b.rfid=d.rfid
                        WHERE a.rfid=getorigrfid2(%s)""", [rfid, rfid, rfid])

    r = cursor.fetchone()
    if r:
        (rfid, cardno, old_cardno, old_rfid, userinfo_rfid, members_rfid, name,
         m_num, utime, realname, m_sex, m_email, m_phone, m_id, m_zip, ppd, mpr) = r

        if m_sex == 1:
            m_sex = 'F'
        elif m_sex == 2:
            m_sex = 'M'
        else:
            m_sex = ''

        if realname:
            names = realname.split()
            if len(names) == 1:
                f_name = names[0]
                l_name = ''
            elif len(names) == 2:
                f_name = names[0].strip()
                l_name = names[1].strip()
            elif len(names) >= 3:
                f_name = names[0].strip()
                l_name = names[2].strip()
        else:
            f_name = ''
            l_name = ''

        m_email = m_email.strip().lower() if m_email else ''

        if not userinfo_rfid and not members_rfid and not utime:
            # blank, never used one
            card_type = 'new'
        elif userinfo_rfid and name and not m_num and not utime:
            # used on console but not registered on the web
            card_type = 'temporary'
        elif (userinfo_rfid == members_rfid) and m_num and m_id:
            # principal card
            card_type = 'principal'
        elif (userinfo_rfid != members_rfid) and m_num and m_id:
            card_type = 'extra'

        return (card_type, rfid, cardno, old_cardno, old_rfid, userinfo_rfid, members_rfid, name,
                m_num, utime, f_name, l_name, m_sex, m_email, m_phone, m_id, m_zip, ppd, mpr)
    else:
        return None


def register_new_card(full_name, rfid):
    cursor = connections['hi'].cursor()
    cursor.execute("""
        INSERT INTO userinfo (name, rfid, homeshop, currshop) values (%s, %s, 5, 5)
        """, [full_name, rfid])
    transaction.commit_unless_managed(using='hi')


def update_temp_card(full_name, rfid):
    cursor = connections['hi'].cursor()
    cursor.execute("""
        UPDATE userinfo set name=%s where rfid=getorigrfid2(%s)
        """, [full_name, rfid])
    transaction.commit_unless_managed(using='hi')


def update_stat(mpr, ppd, rfid):
    cursor = connections['hi'].cursor()
    cursor.execute("UPDATE useravg SET mpr_ta2=%s, ppd_ta2=%s WHERE rfid = getorigrfid2(%s)", [mpr, ppd, rfid])
    transaction.commit_unless_managed(using='hi')


def payment(request, t_id, rfid_id=None):
    context = dict()
    tourney = get_object_or_404(Tournament, id=t_id)
    if rfid_id:
        card = get_object_or_404(Card, rfid=rfid_id)
        entry = Entry.objects.get(tournament=tourney, player=card.player)
        context['entry'] = entry

        membership_fee = entry.balance_membership if entry.balance_membership > 0 else Decimal(0)
        card_fee = entry.balance_card if entry.balance_card > 0 else Decimal(0)
        signup_fee = entry.balance_signup if entry.balance_signup > 0 else Decimal(0)
        due_amount = membership_fee + card_fee + signup_fee

        context['membership_fee'] = membership_fee
        context['card_fee'] = card_fee
        context['signup_fee'] = signup_fee
        context['due_amount'] = due_amount

        # if due_amount == 0:
        #     return HttpResponseRedirect(reverse('22k:entry', args=[t_id]))

        if request.method == 'POST':
            entry.balance_membership = entry.balance_membership - Decimal(request.POST.get('membership_fee'))
            entry.balance_signup = entry.balance_signup - Decimal(request.POST.get('signup_fee'))
            entry.balance_card = entry.balance_card - Decimal(request.POST.get('card_fee'))
            entry.save()

            sms_msg = Template(settings.SMS_MSG['PAYMENT'])
            sms_msg = sms_msg.safe_substitute(name=entry.player.first_name.title(),
                                              amount=due_amount)
            try:
                send_sms(entry.player.phone, sms_msg)
            except:
                pass
            return HttpResponseRedirect(reverse('22k:entry', args=[t_id]))

    elif request.POST.get('rfid_id'):
        return HttpResponseRedirect(reverse('22k:payment', args=[t_id, request.POST['rfid_id']]))
    context['tournament'] = tourney
    return render(request, 'tourney/payment.html', context)


def pre_register_list(request, t_id):
    context = dict()
    tourney = get_object_or_404(Tournament, id=t_id)
    context['tournament'] = tourney
    context['players'] = PreRegPlayer.objects.all()
    return render(request, 'tourney/pre_player.html', context)


def pre_register_create(request, t_id):
    context = dict()
    tourney = get_object_or_404(Tournament, id=t_id)
    context['tournament'] = tourney
    if request.method == 'POST':
        form = PreRegisterForm(request.POST)
        if form.is_valid():
            pre_reg = form.save()
            Entry.objects.create(tournament=tourney, player=pre_reg.player_ptr, balance=-160)
            return HttpResponseRedirect(reverse('22k:pre_register_list', args=[t_id]))
    else:
        form = PreRegisterForm()
    context['form'] = form
    context['tournament'] = tourney
    return render(request, 'tourney/pre_register_create.html', context)


def pre_register(request, t_id, p_id):
    context = dict()
    tourney = get_object_or_404(Tournament, id=t_id)
    context['tournament'] = tourney
    pre_reg = get_object_or_404(PreRegPlayer, id=p_id)
    player = pre_reg.player_ptr
    context['player'] = player
    if request.method == 'POST':
        rfid_id = request.POST.get('rfid_id')
        cardno = _card_number(rfid_id)

        if cardno:
            try:
                card, created = Card.objects.get_or_create(rfid=rfid_id, cardno=cardno, player=player)
            except:
                context['err_msg'] = 'Card(%s) already registered!' % (cardno)
            else:
                return HttpResponseRedirect(reverse('22k:register', args=[t_id, rfid_id]))
    return render(request, 'tourney/pre_register.html', context)


def card(request, t_id):
    context = dict()
    tourney = get_object_or_404(Tournament, id=t_id)
    if tourney.is_over():
        return HttpResponseRedirect(reverse('22k:index'))

    if request.method == 'POST':
        form = CardScanForm(request.POST)
        if form.is_valid():
            try:
                p_num = form.cleaned_data['rfid']
                if len(p_num) == 20:
                    p_rfid = p_num
                elif len(p_num) == 16:
                    try:
                        p_rfid = PhoenixCard(cardno=p_num).get_rfid()
                    except Exception:
                        # bypass exception with vougs rfid
                        p_rfid = '11111111111111111111'
                card = Card.objects.get(Q(rfid=p_rfid) | Q(cardno=p_rfid))
            except Card.DoesNotExist:
                return HttpResponseRedirect(reverse('22k:register', args=[t_id, p_rfid]))
            if card.player.is_registered(t_id):
                return HttpResponseRedirect(reverse('22k:entry', args=[t_id]))
            else:
                return HttpResponseRedirect(reverse('22k:register', args=[t_id, p_rfid]))
    else:
        form = CardScanForm()

    context['form'] = form
    context['tournament'] = tourney
    return render(request, 'tourney/card.html', context)


def register(request, t_id, rfid_id):
    context = dict()
    tourney = get_object_or_404(Tournament, id=t_id)
    context['tournament'] = tourney

    if request.method == 'POST':
        card_posted = {'type': request.POST['card_type'], 'cardno': request.POST['cardno']}

        # see if card is already registered. If so, card has been already used for 22k
        try:
            card = Card.objects.get(rfid=rfid_id)
            player = card.player
            form = RegisterForm(request.POST, instance=player)
            # returning member. update profile
        except Card.DoesNotExist:
            # new member
            form = RegisterForm(request.POST)
            card = Card(cardno=card_posted['cardno'], rfid=rfid_id)

        if form.is_valid():
            # check entry stat

            player_22k = form.save()
            card.player = player_22k
            card.save()

            # if it's pre-registered, change instance
            if player_22k.is_pre_registered():
                player_22k = PreRegPlayer.objects.get(player_ptr=player_22k)

            membership_fee = settings.FEES['MEMBERSHIP'] if not player_22k.is_membership_valid() else 0

            entry, created = Entry.objects.get_or_create(tournament=tourney, player=player_22k)

            membership_credit = Decimal(0)
            signup_credit = Decimal(0)

            if created:

                if player_22k.is_pre_registered():
                    # give credit for pre-registration

                    # sign up credit only for paid more than $15
                    signup_credit = player_22k.credit + (150 - player_22k.credit) if (player_22k.credit - 15) > 0 else 0
                    # check membership credit
                    membership_credit = 15 if player_22k.credit == 115 or player_22k.credit == 135 or player_22k.credit == 15 else 0

                card_fee = settings.FEES['CARD'] if card_posted['type'] == 'new' else 0
                # update balance
                entry.balance_membership = membership_fee - membership_credit
                entry.balance_signup = -signup_credit
                entry.balance_card = card_fee

                # raise Exception(membership_fee)

            # set rank stats
            stats = {'casual_mpr': request.POST.get('casual_stat_mpr'),
                     'casual_ppd': request.POST.get('casual_stat_ppd'),
                     'event_mpr': request.POST.get('event_stat_mpr'),
                     'event_ppd': request.POST.get('event_stat_ppd'),
                     'entry_mpr': request.POST.get('entry_mpr'),
                     'entry_ppd': request.POST.get('entry_ppd')}
            # entry.mpr_rank = Decimal(stats['casual_mpr']) if stats['casual_mpr'] != 'None' else 9
            # entry.ppd_rank = Decimal(stats['casual_ppd']) if stats['casual_ppd'] != 'None' else 60
            entry.mpr_rank = Decimal(stats['casual_mpr']) if stats['casual_mpr'] != 'None' else 0
            entry.ppd_rank = Decimal(stats['casual_ppd']) if stats['casual_ppd'] != 'None' else 0
            # set tournament stats
            entry.mpr_event = Decimal(stats['entry_mpr']) if stats['entry_mpr'] else 0
            entry.ppd_event = Decimal(stats['entry_ppd']) if stats['entry_ppd'] else 0
            entry.save()

            # update casual stat with tournament stat
            player_22k.update_stat(entry.mpr_event, entry.ppd_event)

            row = {}
            row['sex'] = player_22k.gender
            row['name'] = player_22k.full_name
            row['mobile'] = player_22k.phone
            row['mpr'] = str(entry.mpr_event)
            row['ppd'] = str(entry.ppd_event)
            row['cardno'] = card.cardno
            # row['entry'] = entry.balance_card  # if he is not member else '$0'
            # row['card'] = '$5'  # if he has not his card else '$0'
            if settings.GOOGLE_DOC['SYNC']:
                sheet = gdrive.Sheet(settings.GOOGLE_DOC['BOOK_NAME'], 'Entry')
                sheet.insert(row)
            # sheet.delete_all()

            #register new card and update temp card nickname
            if card_posted['type'] == 'new':
                register_new_card(player_22k.full_name, rfid_id)
            elif card_posted['type'] == 'temporary':
                update_temp_card(player_22k.full_name, rfid_id)

            # mark pre_registered list
            if player_22k.is_pre_registered():
                player_22k.is_registered = True
                player_22k.save()

            # overwrite player nick name with full name
            update_temp_card(player_22k.full_name, rfid_id)

            # text welcome message
            sms_msg = Template(settings.SMS_MSG['REGISTRATION'])
            sms_msg = sms_msg.safe_substitute(name=player_22k.first_name.title(),
                                              tournament_title=tourney.title)
            if created:
                try:
                    send_sms(player_22k.phone, sms_msg)
                except:
                    pass
            return HttpResponseRedirect(reverse('22k:entry', args=(t_id,)))

        context['event_stat'] = {'MPR': request.POST.get('event_stat_mpr'), 'PPD': request.POST.get('event_stat_ppd')}
        context['casual_stat'] = {'MPR': request.POST.get('casual_stat_mpr'), 'PPD': request.POST.get('casual_stat_ppd')}
        context['card_type'] = card_posted['type']
        context['card'] = card
        context['form'] = form
        return render(request, 'tourney/register.html', context)

    else:
        if len(rfid_id) < 20:
            context['card_type'] = None
            return render(request, 'tourney/register.html', context)
        # see if card already registered

        card_info = _card_info(rfid_id)
        if not card_info:
        # invalid card scanned
            context['card_type'] = None
            return render(request, 'tourney/register.html', context)

        # valid card scanned. get card info from maindb
        (card_type, rfid, cardno, old_cardno, old_rfid, userinfo_rfid, members_rfid, name,
         m_num, utime, f_name, l_name, m_sex, m_email, m_phone, m_id, m_zip, ppd, mpr) = card_info

        last_entries = []

        if card_type == 'new':
            # blank, never used one
            card = Card(cardno=cardno, rfid=rfid_id)
            player = Player()
        else:

            try:
                # check if 22K member
                card = Card.objects.get(rfid=rfid_id)
                player = card.player

                # populate userinfo from main db
                player.user_id = m_id if not player.user_id and m_id else player.user_id
                player.gender = m_sex if not player.gender and m_sex else player.gender
                player.email = m_email if not player.email and m_email else player.email
                player.phone = m_phone if not player.phone and m_phone else player.phone
                player.zipcode = m_zip if not player.zipcode and m_zip else player.zipcode

                # get previous entry
                last_entries = player.entry_set.all()

            except Card.DoesNotExist:
                # not 22k member
                card = Card(cardno=cardno, rfid=rfid_id)
                player = Player(user_id=m_id,
                                first_name=f_name,
                                last_name=l_name,
                                gender=m_sex,
                                phone=m_phone,
                                email=m_email,
                                zipcode=m_zip
                                )
                card.player = player
        context['card'] = card
        context['card_type'] = card_type
        context['screen_name'] = name
        context['player'] = player
        context['last_entries'] = last_entries
        context['form'] = RegisterForm(instance=player)
        context['event_stat'] = player.event_stat()
        mpr = mpr if mpr > 0 else None
        ppd = ppd if ppd > 0 else None
        context['casual_stat'] = {'MPR': mpr, 'PPD': ppd}
    return render(request, 'tourney/register.html', context)


def print_signup_receipt(team, event):
    # print signup recepits
    try:
        # receipt = brother.Label(ip_address=settings.PRINTER['BROTHER_RECEIPT'])
        receipt = brother.Label(ip_address=settings.PRINTER['BROTHER_LABEL'], port=9200)
        # receipt.print_singles(event.title, team.name, 'MPR: %s / PPD: %s' % (team.mpr_rank, team.ppd_rank))
        receipt.print_line(event.tournament.title, size=50)
        receipt.print_line('', size=50)
        receipt.print_line('Event: %s' % (event.title))
        receipt.print_line('', size=50)
        receipt.print_line('Team: %s' % (team.name))
        # receipt.print_line('Stat(ppd/mpr): %s / %s' % (team.ppd_rank, team.mpr_rank))
        receipt.print_line('', size=50)
        receipt.print_line('%s' % (datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        receipt.cut()
    except:
        pass

def print_bracket_label(team, event):
    # print signup recepits
    try:
        receipt = brother.Label(ip_address=settings.PRINTER['BROTHER_LABEL'], port=9200)
        receipt.print_singles(team.name, event.title, 'MPR: %s / PPD: %s' % (team.mpr_rank, team.ppd_rank))
    except:
        pass
    # receipt.cut()
    # receipt.print_line(team.name)
    # receipt.print_line('MPR: %s / PPD: %s' % (team.mpr_rank, team.ppd_rank))
    # receipt.cut()

def _validate_card_scan(rfids, unique=True):
    if unique and len(set(rfids)) != len(rfids):
        return  False
    for rfid in rfids:
        if not rfid.isdigit() or len(rfid) != 20:
            return False
    return True

def _need_to_pay(players, event):
    for entry in Entry.objects.filter(player__in=players, tournament=event.tournament):
        return True if entry.balance > 0 else False

def event_signup(request, e_id):
    context = dict()
    event = get_object_or_404(Event, id=e_id)

    if request.method == 'POST':
        rfids = filter(None, [request.POST.get('card1'), request.POST.get('card2'), request.POST.get('card3')])
        entry_ids = request.POST.getlist('entry_id')

        # Validation step is done. finish signup
        if len(entry_ids) > 0:
            players = [Entry.objects.get(pk=entry_id).player for entry_id in entry_ids]

            # Okay to procced to sign up
            if event.is_lotd():
                # blind draw event. add player to drawentry
                for player in players:
                    DrawEntry.objects.get_or_create(event=event, player=player)
                    messages.success(request, '%s signed up successfully.' % (player.full_name))
            else:
                # singles or bring event. create a team
                team_name = ', '.join(player.full_name for player in players)
                team, created = Team.objects.get_or_create(event=event, name=team_name)
                if created:
                    for player in players:
                        team.players.add(player)

                        rank_mpr = player.stat_rank(event.tournament)['MPR']
                        rank_ppd = player.stat_rank(event.tournament)['PPD']

                        team.mpr_rank += rank_mpr
                        team.ppd_rank += rank_ppd

                    # cacluate average
                    team.mpr_rank = team.mpr_rank / len(players)
                    team.ppd_rank = team.ppd_rank / len(players)
                    team.save()
                messages.success(request, 'Team - %s signed up successfully.' % (team.name))
                # print signup recepits
            if settings.PRINTER['LIVE']:
                team = Team(name=player) if event.is_lotd() else team
                print_signup_receipt(team, event)
                # print_bracket_label(team, event)

            # book signup fee payment record
            SignupPayment.objects.filter(player__in=players, event=event).update(paid=True)
            # reset entry balance
            Entry.objects.filter(id__in=entry_ids).update(balance_card=0, balance_membership=0, balance_signup=0)

        else:
            # Start validation
            # Validate RFIDs
            if not _validate_card_scan(rfids) or len(set(rfids))!= event.team_size():
                messages.error(request, 'Invalid or duplicate RFIDs. Check the cards and try again.')
                return HttpResponseRedirect(reverse('22k:event_signup', args=[e_id]))

            # Check if card/player registered
            players = []
            for rfid in rfids:
                reg_url = reverse('22k:register', args=[event.tournament_id, rfid])
                try:
                    player = Card.objects.get(rfid=rfid).player
                    players.append(player)
                except ObjectDoesNotExist:
                    #player with the card has not been registered yet!
                    messages.error(request, 'Card is not registered yet. <a href="%s">Click here to register</a>' % (reg_url))
                    # return HttpResponseRedirect(reverse('22k:register', args=[event.tournament_id, rfid]))
                    return HttpResponseRedirect(reverse('22k:event_signup', args=[e_id]))
                else:
                    if not player.is_registered(event.tournament):
                        messages.error(request, '%s is not registered yet. <a href="%s">Click here to register</a>' % (player, reg_url))
                        return HttpResponseRedirect(reverse('22k:event_signup', args=[e_id]))


            # Check players are qualifeid for the event
            for player in players:
                if event.is_official() and not player.is_qualified(event.tournament):
                    messages.error(request, '%s is NOT qualified for this event!' % (player.full_name))
                    return HttpResponseRedirect(reverse('22k:event_signup', args=[e_id]))
                elif event.is_ladies_event() and not player.is_lady():
                    messages.error(request, '%s is not allowed for ladies event' % (player.full_name))
                    return HttpResponseRedirect(reverse('22k:event_signup', args=[e_id]))

            # Check players are already signed up/ and make entry list
            for player in players:
                if event.is_lotd():
                    if event.drawentry_set.filter(player=player).exists():
                        messages.error(request, '%s has already signed up!' % (player.full_name))
                        return HttpResponseRedirect(reverse('22k:event_signup', args=[e_id]))
                else:
                    if event.team_set.filter(players=player).exists():
                        messages.error(request, '%s has already signed up!' % (player.full_name))
                        return HttpResponseRedirect(reverse('22k:event_signup', args=[e_id]))

            # Check signup fee payment
            entries = Entry.objects.filter(player__in=players, tournament=event.tournament)
            for entry in entries:
                if entry.qualified:
                    try:
                        pre_reg = PreRegVegas.objects.get(player_id=entry.player.id)
                        context['pre_reg'] = pre_reg
                    except:
                        pass

                signup_payment, created = SignupPayment.objects.get_or_create(player=player, event=event)
                if created:
                    if not signup_payment.paid:
                        entry.balance_signup = entry.balance_signup + event.signup_fee
                        entry.save()
                        messages.info(request, 'Collect payment to finish the signup.')
                elif signup_payment.paid:
                    messages.info(request, '%s' % signup_payment)

            context['entries'] = entries

        # if event.draw != 'L':
        #     team = Team(event=event)
        #     if len(players) < 3 and event.draw != 'L':
        #         team.name = ', '.join(player.full_name for player in players)
        #     else:
        #         team.name = request.POST.get('teamname')
        #     team.save()
        # for player in players:
        #     entry = player.entry_set.get(tournament=event.tournament)
        #     if event.draw == 'L':
        #         DrawEntry.objects.create(event=event, player=player)
        #     else:
        #         team.players.add(player)

        #         rank_mpr = player.stat_rank(event.tournament)['MPR']
        #         rank_ppd = player.stat_rank(event.tournament)['PPD']

        #         # entry.mpr_rank = rank_mpr
        #         # entry.ppd_rank = rank_ppd

        #         team.mpr_rank += rank_mpr
        #         team.ppd_rank += rank_ppd

        #     # charge sign up fee
        #     entry.balance_signup = F('balance_signup') + settings.FEES['SIGNUP']
        #     entry.save()

        #     sms_msg = Template(settings.SMS_MSG['SIGNUP'])
        #     sms_msg = sms_msg.safe_substitute(name=player.first_name.title(),
        #                                       event_title=event.title,
        #                                       start_at=event.start_at.strftime("%I:%M %p"))
        #     try:
        #         send_sms(player.phone, sms_msg)
        #     except:
        #         pass
        # if event.draw == 'L':
        #     messages.success(request, '%s singned up successfully.' % (players[0].full_name))
        # else:
        #     messages.success(request, '%s singned up successfully.' % (team.name))
        #     #cacluate average
        #     team.mpr_rank = team.mpr_rank / len(players)
        #     team.ppd_rank = team.ppd_rank / len(players)
        #     team.save()

        #     if settings.GOOGLE_DOC['SYNC']:
        #         sheet = gdrive.Sheet(settings.GOOGLE_DOC['BOOK_NAME'], 'Signup')
        #         sheet.insert({'team': team.name, 'mpr': str(team.mpr_rank), 'ppd': str(team.ppd_rank)})

        #     # print signup recepits
        #     if settings.PRINTER['LIVE']:
        #         print_signup_receipt(team, event)
        #         print_bracket_label(team, event)

    context['tournament'] = event.tournament
    context['event'] = event
    if event.is_lotd():
        context['draw_entry'] = DrawEntry.objects.filter(event=event)
    else:
        context['teams'] = event.team_set.all()
    return render(request, 'tourney/event_signup.html', context)

def event_signup2(request, e_id):
    context = dict()
    event = get_object_or_404(Event, id=e_id)
    if request.method == 'POST':
        rfids = filter(None, [request.POST.get('card1'), request.POST.get('card2'), request.POST.get('card3')])
        #check if there is duplicate player in the team
        context['error_msg'] = 'ERROR: duplicate card number. Try again' if len(rfids)!=len(set(rfids)) else ''
        for rfid in rfids:
            context['error_msg'] = 'ERROR: player(card) has not been registered yet!' if Player.objects.filter(card__rfid=rfid).count() == 0 else ''
    context['tournament'] = event.tournament
    context['event'] = event
    context['total_signup'] = event.team_set.count()
    return render(request, 'tourney/event_signup2.html', context)


def is_player_signup_any_event(t_id, entry_id):
    e = Entry.objects.get(pk=entry_id)
    tc = Team.objects.filter(players__in=[e.player], event__in=Event.objects.filter(tournament_id=t_id)).count()
    dc = DrawEntry.objects.filter(player=e.player, event__in=Event.objects.filter(tournament_id=t_id)).count()
    if tc or dc:
        return True
    else:
        return False


def del_entry(request, t_id, entry_id):
    e = Entry.objects.get(pk=entry_id)

    if not is_player_signup_any_event(t_id, entry_id):
        e.delete()
        # messages.info(request, '%s has beeen deleted.' % (e.player))
    else:
        messages.error(request, '%s already signed up and can not be deleted.' %(e.player))

    return HttpResponseRedirect(reverse('22k:entry', args=(t_id,)))


def del_team(request, e_id, team_id):
    try:
        Team.objects.get(pk=team_id).delete()
    except DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('22k:event_signup', args=(e_id,)))

def del_signup(request, e_id, s_id):
    e = get_object_or_404(Event, id=e_id)
    if e.is_lotd():
        try:
            d = DrawEntry.objects.get(pk=s_id)
            d.delete()
            messages.info(request, '%s cancelled signup' % (d.player.full_name))
        except ObjectDoesNotExist:
            pass
    else:
        try:
            t = Team.objects.get(pk=s_id)
            t.delete()
            messages.info(request, '%s cancelled signup' % (t.name))
        except ObjectDoesNotExist:
            pass
    return HttpResponseRedirect(reverse('22k:event_signup', args=(e_id,)))

def draw(request, e_id):
    from random import shuffle

    context = dict()
    event = get_object_or_404(Event, id=e_id)
    tourney = event.tournament
    context['tournament'] = tourney
    if event.draw != 'L':
        context['err_msg'] = "Event( %s ) is not a 'Luck of The Draw' event" % (event.title)
        return render(request, 'tourney/event_draw.html', context)
    elif event.is_drawn():
        context['err_msg'] = "Event( %s ) is already drawed!" % (event.title)
        return render(request, 'tourney/event_draw.html', context)

    entry = DrawEntry.objects.filter(event=event)
    n = len(entry)
    half = n/2
    quater = half/2
    high = []
    low = []
    mhigh = []
    mlow = []
    for i in range(0, quater):
        high.append(entry[i].player)
        low.append(entry[i + n - quater].player)

    for i in range(quater, half):
        mhigh.append(entry[i].player)
        mlow.append(entry[i - quater + half].player)

    shuffle(high)
    shuffle(low)
    shuffle(mhigh)
    shuffle(mlow)

    Team.objects.filter(event=event).delete()
    for i in range(0, len(high)):
        team = Team.objects.create(event=event)
        team.players.add(high[i])
        team.players.add(low[i])
        team.name = ', '.join([high[i].full_name, low[i].full_name])
        team.mpr_rank = (high[i].stat_rank(tourney)['MPR'] + low[i].stat_rank(tourney)['MPR']) / 2
        team.ppd_rank = (high[i].stat_rank(tourney)['PPD'] + low[i].stat_rank(tourney)['PPD']) / 2
        team.save()

    for i in range(0, len(mhigh)):
        team = Team.objects.create(event=event)
        team.players.add(mhigh[i])
        team.players.add(mlow[i])
        team.name = ', '.join([mhigh[i].full_name, mlow[i].full_name])
        team.mpr_rank = (mhigh[i].stat_rank(tourney)['MPR'] + mlow[i].stat_rank(tourney)['MPR']) / 2
        team.ppd_rank = (mhigh[i].stat_rank(tourney)['PPD'] + mlow[i].stat_rank(tourney)['PPD']) / 2
        team.save()
    #_save_gdoc(event)
    return HttpResponseRedirect(reverse('22k:event_signup', args=(event.id,)))


def _save_gdoc(event):
    return
    import bracket
    # import gdrive

    sort_order = 'mpr_rank' if event.game == 'CR' or event.game == 'Medley' else 'ppd_rank'
    team_ranked = event.team_set.all().order_by(sort_order)
    teams = {}
    for i in range(0, len(team_ranked)):
        teams.update({str(i+1): str(team_ranked[i])})

        _bracket = bracket.Bracket(teams)

        sheet = gdrive.Sheet(settings.GOOGLE_DOC['BOOK_NAME'], settings.GOOGLE_DOC['SHEET_NAME'])
        sheet.delete_all()

    for i in range(1, 33):
        for j in [0, 1]:
            id = _bracket.match[i]['teams'][j]
            dct = {'number': "%03d00%03d" % (i, id), 'team': teams[str(id)]}
            sheet.insert( dct )


def league_stat(request):
    context = {}
    # if request.method == 'POST':

    # else:

    return render(request, 'tourney/league_stat.html', context)


def refree(request, e_id):
    import gdrive
    import bracket

    context = {}
    event = get_object_or_404(Event, id=e_id)
    context['event'] = event
    context['icon_select'] = ['<i class="icon-lock" title="Stu Pae, Isaac Hans"></i>', '']

    sort_order = 'mpr_rank' if event.game == 'CR' else 'ppd_rank'
    team_ranked = event.team_set.all().order_by(sort_order)
    teams = {}
    for i in range(0, len(team_ranked)):
        teams.update({str(i+1): str(team_ranked[i])})

    _bracket = bracket.Bracket(teams)

    # sheet = gdrive.Sheet(settings.GOOGLE_DOC['BOOK_NAME'], settings.GOOGLE_DOC['SHEET_NAME'])
    # sheet.delete_all()

    # for i in range(1, 33):
    #     for j in [0, 1]:
    #         id = _bracket.match[i]['teams'][j]
    #         dct = { 'number': "%03d00%03d" % (i, id), 'team': teams[str(id)]}
    #         sheet.insert( dct )

    # for i in range(1, 49) + range(1, 33)  + range(1, 9) + range(1, 5) + range(1, 3):
    #     _bracket.report(i)


    matches = _bracket.match

    player_pos = [None]

    for i in range(1, 33):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
    for i in range(1, 33):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])

    # Rond 2 Winners
    for i in range(33, 49):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
            player_pos.append(None)
    for i in range(33, 49):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
            player_pos.append(None)

    # Rond 3 Winners
    for i in range(49, 57):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
            player_pos.append(None)
    for i in range(49, 57):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
            player_pos.append(None)

    # Round 4
    for i in range(57, 61):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
            player_pos.append(None)
    for i in range(57, 61):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
            player_pos.append(None)

    # Round 5 Winners
    for i in range(61, 63):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
            player_pos.append(None)
    for i in range(61, 63):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
            player_pos.append(None)

    # Round 6 Winners
    for i in range(63, 64):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
            player_pos.append(None)
    for i in range(63, 64):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
            player_pos.append(None)

    # Round 2 Loosers
    for i in range(64, 80):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
             player_pos.append(None)
    for i in range(64, 80):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
            player_pos.append(None)

    # Round 3 Loosers
    for i in range(80, 96):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
             player_pos.append(None)

    for i in range(80, 96):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
             player_pos.append(None)

    # Round 4 Loosers
    for i in range(96, 104):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
             player_pos.append(None)

    for i in range(96, 104):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
             player_pos.append(None)

    # # Round 5 Loosers
    for i in range(104, 112):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
             player_pos.append(None)

    for i in range(104, 112):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
             player_pos.append(None)

    for i in range(112, 116):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
             player_pos.append(None)

    for i in range(112, 116):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
             player_pos.append(None)

    for i in range(116, 120):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
             player_pos.append(None)

    for i in range(116, 120):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
             player_pos.append(None)

    for i in range(120, 122):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
             player_pos.append(None)

    for i in range(120, 122):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
             player_pos.append(None)

    for i in range(122, 124):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
             player_pos.append(None)

    for i in range(122, 124):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
             player_pos.append(None)

    for i in range(124, 125):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
             player_pos.append(None)

    for i in range(124, 125):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
             player_pos.append(None)

    for i in range(125, 126):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
             player_pos.append(None)

    for i in range(125, 126):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
             player_pos.append(None)

    for i in range(126, 127):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
             player_pos.append(None)

    for i in range(126, 127):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
             player_pos.append(None)

    for i in range(127, 128):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][0])
        else:
             player_pos.append(None)

    for i in range(127, 128):
        if matches[i]['teams']:
            player_pos.append(matches[i]['teams'][1])
        else:
             player_pos.append(None)

    context['matches'] = teams
    context['player_pos'] = player_pos
    return render(request, 'tourney/bracket.html', context)


def game_result(request, rfid=None):
    context = dict()
    cursor = connections['hi'].cursor()

    if rfid:
        sql = """select to_char(a.ctime, 'mm-dd hh:mi:ss AM' ) as ended_at, gameid, b.name, ppdmpr, teamtype, sameteam,
                      iswin, a.rfid from v_gamedata3 a join userinfo b on a.rfid=b.rfid
                      where shopid=209 and a.rfid=%s  order by gametype, gameid, sameteam""" % (rfid)
    else:
        sql = """select to_char(a.ctime, 'mm-dd hh:mi:ss AM' ) as ended_at, gameid, b.name, ppdmpr, teamtype, sameteam,
                      iswin, a.rfid
                      from v_gamedata3 a join userinfo b on a.rfid=b.rfid where shopid=209 order by gameid, sameteam"""

    cursor.execute(sql)
    r = cursor.fetchall()
    context['games'] = r
    return render(request, 'tourney/game_result.html', context)

def stat_monitor(request):
    context = dict()
    cursor = connections['hi'].cursor()
    sql = """select b.rfid, a.name, b.tourney,
    case when gametype=2 then c.ppd_ta2
         when gametype=7 then c.mpr_ta2
    end as casual,
    case when gametype=2 then c.ppd_ta2 - tourney
         when gametype=7 then c.mpr_ta2 - tourney
    end as diff
    , b.gc

from userinfo a join (select rfid, gametype, count(*) as gc, trunc(avg(ppdmpr)::numeric, 2) as tourney
from v_gamedata where shopid=209 and gameid not in (222295) group by rfid, gametype)as b on a.rfid=b.rfid
join useravg c on a.rfid=c.rfid

where gc > 1 and b.rfid > 1 and b.rfid not in (16142028065945800250, 16142028065945803797) order by gametype, diff desc"""
    cursor.execute(sql)
    r = cursor.fetchall()
    context['games'] = r
    return render(request, 'tourney/stat_monitor.html', context)


def lg_qualify_point(league_card):
    cursor = connections['hi'].cursor()
    # sql = """
    # select d.name, c.name, e.name, count(distinct a.scheduleid) * 4 as point, e.cardno from ml.lineup a
    # join ml.schedule b on a.scheduleid = b.scheduleid
    # join ml.luserinfo e on e.rfid = a.rfid
    # left join ml.league c on b.leagueid = c.leagueid
    # left join pxprogram.dealers d on d.num = c.dealerid

    # where b.isdone = 1 and c.dealerid !=1
    # group by a.rfid, d.name, c.name, e.name, e.cardno
    # order by d.name, c.name, e.name, point
    # """

    sql = """
    select count(distinct a.scheduleid)*4 as point from ml.lineup a
    join ml.schedule b on a.scheduleid = b.scheduleid
    join ml.luserinfo e on e.rfid = a.rfid
    where b.isdone = 1 and e.cardno='%s'
    group by a.rfid
    """ % (league_card)
    cursor.execute(sql)
    r = cursor.fetchone()
    return r

def lg_player_info(league_card):
    cursor = connections['hi'].cursor()
    sql = """
    select name, nickname from ml.luserinfo where cardno='%s'
    """ % (league_card)
    cursor.execute(sql)
    r = cursor.fetchone()
    return r


def qualify_point(request):
    context = dict()
    if request.method == 'POST':
        form = QualifyForm(request.POST)
        if form.is_valid():
            lg_card = form.cleaned_data['league_card']
            r = lg_player_info(lg_card)
            if r:
                context['player'] = {'name': r[0], 'nickname': r[1]}
                subs_point = int(form.cleaned_data['subs']) * 4 if form.cleaned_data['subs'] else 0
                pc22k_point = int(form.cleaned_data['pc22k']) * 2 if form.cleaned_data['pc22k'] else 0
                context['point'] = int(lg_qualify_point(lg_card)[0]) + subs_point + pc22k_point

    else:
        form = QualifyForm()
    context['form'] = form
    return render(request, 'tourney/100k.html', context)

