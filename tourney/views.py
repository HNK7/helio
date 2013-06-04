from django.conf import settings
from django.db import connections, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from tourney.models import Tournament, Event, Player, Entry, Card
from tourney.forms import TournamentForm, EventForm, RegisterForm, ProfileForm, EntryForm
# import gdata.spreadsheet.service


def index(request):
    tournament_list = Tournament.objects.all().order_by('-start_at')
    context = {'tournament_list': tournament_list}
    return render(request, 'tourney/index.html', context)


def tourney_dashboard(request, t_id):
    context = dict()
    tournament = get_object_or_404(Tournament, pk=t_id)
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


def event_signup(request, e_id):
    context = dict()
    event = get_object_or_404(Event, id=e_id)

    context['tournament'] = event.tournament
    context['event'] = event
    context['teams'] = event.teams.all()
    return render(request, 'tourney/event_signup.html', context)


def detail(request, t_id):
    tournament = get_object_or_404(Tournament, pk=t_id)
    return render(request, 'tourney/view.html', {'tournament': tournament})


def player(request):
    context = dict()
    context['tournament_list'] = Tournament.objects.all()

    players = Player.objects.all()
    context['players'] = players
    context['player_total'] = len(players)
    return render(request, 'tourney/player.html', context)


def entry(request, t_id):
    context = dict()
    context['tournament_list'] = Tournament.objects.all()
    tourney = get_object_or_404(Tournament, pk=t_id)
    context['tournament'] = tourney

    entry = tourney.players.all()
    context['entry'] = entry
    context['entry_total'] = len(entry)
    return render(request, 'tourney/entry.html', context)


def profile(request, p_id):
    context = dict()
    context['tournament_list'] = Tournament.objects.all()
    player = Player.objects.get(id=p_id)
    casual_stat = player.casual_stat()
    # ranking_stat = player.ranking()
    event_stat = player.event_stat()
    entries = player.entry_set.all()

    context['player'] = player
    context['entries'] = entries
    context['ppd_casual'] = casual_stat['PPD']
    context['mpr_casual'] = casual_stat['MPR']
    # context['ppd_ranking'] = ranking_stat['PPD']
    # context['mpr_ranking'] = ranking_stat['MPR']
    context['ppd_event'] = event_stat['PPD']
    context['mpr_event'] = event_stat['MPR']
    return render(request, 'tourney/profile.html', context)


def profile_edit(request, p_id):
    context = dict()
    context['tournament_list'] = Tournament.objects.all()
    player = get_object_or_404(Player, id=p_id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('22k:profile', args=(p_id,)))

    else:
        form = ProfileForm(instance=player)
    context['form'] = form
    context['player'] = player
    return render(request, 'tourney/profile_edit.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # if form.is_valid():
            # form.save()
            # return HttpResponseRedirect('/')
        return HttpResponseRedirect('/22k')
    else:
        form = RegisterForm()

    context = dict()
    context['tournament_list'] = Tournament.objects.all()
    context['form'] = form
    return render(request, 'tourney/register.html', context)


def _insert_google_doc(row):
    gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    gd_client.email = 'phoenix@dartoo.com'
    gd_client.password = '3355dartoO'
    gd_client.source = '22K'
    gd_client.ProgrammaticLogin()
    spreadsheet_key = 'tVc9gCzhh-seVwvaojke4Iw'
    feed = gd_client.GetWorksheetsFeed(spreadsheet_key)
    worksheet_id = 'od6'
    for entry in feed.entry:
        if entry.title.text == 'Entry':
            worksheet_id = entry.id.text.rsplit('/', 1)[1]

    row = {}
    row['sex'] = 'm'
    row['name'] = 'John Kuczinksy'
    row['mobile'] = '2134223214'
    row['mpr'] = '3.4'
    row['ppd'] = '34.24'
    row['cardno'] = '12432155533'
    row['entry'] = '$15'  # if he is not member else '$0'
    row['card'] = '$5'  # if he has not his card else '$0'

    try:
        entry = gd_client.InsertRow(row, spreadsheet_key, worksheet_id)
    except Exception, e:
        print "Error %s inserting" % (e, )
    #     return False
    # entry = gd_client.InsertRow(row, spreadsheet_key, worksheet_id)
    if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
        return True


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
        UPDATE userinfo set name=%s where rfid=%s
        """, [full_name, rfid])
    transaction.commit_unless_managed(using='hi')


def card(request, rfid_id):
    context = dict()
    if request.method == 'POST':
        card_posted = {'type': request.POST['card_type'], 'cardno': request.POST['cardno']}

        # see if card is already registered. If so, card has been already used for 22k
        try:
            card = Card.objects.get(rfid=rfid_id)
            player = card.owned
            form = RegisterForm(request.POST, instance=player)
            # returning member. update profile
        except ObjectDoesNotExist:
            # new member
            form = RegisterForm(request.POST)
            card = Card(cardno=card_posted['cardno'], rfid=rfid_id)

        if form.is_valid():
            player_22k = form.save()
            card.owned = player_22k
            card.save()

            tourney = Tournament.objects.latest('start_at')
            entry, created = Entry.objects.get_or_create(tournament=tourney, player=player_22k)
            membership_fee = settings.FEES['MEMBERSHIP'] if created else 0
            card_fee = settings.FEES['CARD'] if created and card_posted['type'] == 'new' else 0

            # update balance
            player_22k.balance = player_22k.balance + membership_fee + card_fee
            player_22k.save()

            #register new card and update temp card nickname
            if card_posted['type'] == 'new':
                register_new_card(player_22k.full_name, rfid_id)
            elif card_posted['type'] == 'temporary':
                update_temp_card(player_22k.full_name, rfid_id)

            return HttpResponseRedirect('/22k')

        context['card_type'] = card_posted['type']
        context['card'] = card
        context['form'] = form
        return render(request, 'tourney/card.html', context)

    else:
        card_info = _card_info(rfid_id)
        if not card_info:
        # invalid card scanned
            context['card_type'] = None
            return render(request, 'tourney/card.html', context)
        else:
        # valid card scanned. get card info from maindb
            (card_type, rfid, cardno, old_cardno, old_rfid, userinfo_rfid, members_rfid, name,
             m_num, utime, f_name, l_name, m_sex, m_email, m_phone, m_id, m_zip, ppd, mpr) = card_info

            if card_type == 'new':
                # blank, never used one
                card = Card(cardno=cardno, rfid=rfid_id)
                player = Player()
            else:

                try:
                    # check if 22K member
                    card = Card.objects.get(rfid=rfid_id)
                    player = card.owned

                    # populate userinfo from main db
                    player.user_id = m_id if not player.user_id and m_id else player.user_id
                    player.gender = m_sex if not player.gender and m_sex else player.gender
                    player.email = m_email if not player.email and m_email else player.email
                    player.phone = m_phone if not player.phone and m_phone else player.phone
                    player.zipcode = m_zip if not player.zipcode and m_zip else player.zipcode

                except ObjectDoesNotExist:
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
                    card.owned = player

            context['card'] = card
            context['card_type'] = card_type
            context['screen_name'] = name
            context['player'] = player
            context['form'] = RegisterForm(instance=player)
            context['event_stat'] = player.event_stat()
            context['casual_stat'] = {'MPR': mpr, 'PPD': ppd}
        return render(request, 'tourney/card.html', context)
