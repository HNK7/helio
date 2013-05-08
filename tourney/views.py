from django.db import connections
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from tourney.models import Tournament, Player, Entry, Card
from tourney.forms import RegisterForm, ProfileForm, EntryForm
# import gdata.spreadsheet.service


def index(request):
    tournament_list = Tournament.objects.all()
    context = {'tournament_list': tournament_list}
    return render(request, 'tourney/index.html', context)


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
    ranking_stat = player.ranking()
    event_stat = player.event_stat()

    context['player'] = player
    context['ppd_casual'] = casual_stat['PPD']
    context['mpr_casual'] = casual_stat['MPR']
    context['ppd_ranking'] = ranking_stat['PPD']
    context['mpr_ranking'] = ranking_stat['MPR']
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
    cursor.execute("""SELECT b.rfid, %s, name, cardno, realname, m_sex, m_email, m_phone
                FROM userinfo a
                join  members b on a.rfid=b.rfid
                where b.rfid = getorigrfid2(%s)""", (rfid, rfid))
    r = cursor.fetchone()
    return {'org_rfid': r[0], 'card_rfid': int(r[1]),
            'name': r[2], 'cardno': r[3], 'realname': r[4], 'gender': r[5],
            'email': r[6], 'phone': r[7]}


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


def _draw_stat(p):
    e_stat = p.event_stat()
    c_stat = p.casual_stat()
    r_stat = p.ranking()

    if e_stat:
        stat = e_stat
    elif r_stat:
        stat = r_stat
    else:
        stat = c_stat
    return stat


def _card_number(rfid):
    cursor = connections['hi'].cursor()
    cursor.execute("SELECT cardno FROM checkrfid where rfid=%s", [rfid, ])
    r = cursor.fetchone()
    return r[0]


def card(request, rfid_id):
    if request.method == 'POST':
        # try:
        #     card = Card.objects.get(rfid=rfid_id)
        #     # player = Player.objects.get(id=card.owned)
        form = EntryForm(request.POST)

        # except Player.DoesNotExist:
        #     form = EntryForm(request.POST)
        card = Card(rfid=request.POST['rfid'], cardno=request.POST['cardno'])
        if form.is_valid():
            # take care of copied card
            # form.save(commit=False)
            # f_rfid = form.cleaned_data['rfid']
            # userinfo = _userinfo(f_rfid)
            # # replace rfid with orginal one
            # form.cleaned_data['rfid'] = userinfo['org_rfid']
            p = form.save()
            tourney = Tournament.objects.get(id=2)
            tourney.entry_set.add(Entry(tournament=tourney, player=p))
            card.owned_id = p.id
            # card.save()
            # Tournament.objects.all()[1].entry_set.add(p)
            # cursor = connections['hi'].cursor()
            # cursor.execute("insert into tourney_entry (tournament_id, player_id) values (%s, %s)" % (2, player.id))

            # player = Player.objects.get(rfid=userinfo['org_rfid'])
            # stat = _draw_stat(player)

            # row = {}
            # card_fee = 0
            # entry_fee = 0
            # row['sex'] = player.gender
            # row['name'] = player.full_name
            # row['mobile'] = player.phone
            # row['mpr'] = stat['MPR']
            # row['ppd'] = stat['PPD']
            # row['cardno'] = player.cardno

            # # if new card
            # if not userinfo:
            #     card_fee = 5
            # if not player:
            #     entry_fee = 15

            # row['entry'] = '$%s' % (entry_fee)  # if he is not member else '$0'
            # row['card'] = '$%s' % (card_fee,)  # if he has not his card else '$0'
            # _insert_google_doc(row)
            return HttpResponseRedirect('/22k/entry/2')
    else:
        if len(rfid_id) < 20 or int(rfid_id) < 16000000000000000000:
            return HttpResponseRedirect('/22k/entry/2')
        try:
            card = Card.objects.get(rfid=rfid_id)
            player = Player.objects.get(id=card.owned_id)
            return HttpResponseRedirect('22k/player/%s' % player.id)
        except Card.DoesNotExist:
            player = Player()
            userinfo = _userinfo(rfid_id)

            full_name = userinfo['realname'].split()
            player.first_name = full_name[0].title()
            if len(full_name) == 2:
                player.last_name = full_name[1].title()
            else:
                player.last_name= full_name[-1].title()
            sex = ['','F', 'M']
            player.gender = sex[userinfo['gender']]
            player.email = userinfo['email'].lower()
            player.phone = userinfo['phone']

            card = Card(cardno=userinfo['cardno'], rfid=userinfo['org_rfid'])
            form = EntryForm(instance=player)

    context = dict()
    msg = ''
    context['tournament_list'] = Tournament.objects.all()
    context['msg'] = msg
    context['form'] = form
    context['card'] = card
    return render(request, 'tourney/card.html', context)
