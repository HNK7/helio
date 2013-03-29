from django.db import connections
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from tourney.models import Tournament, Player
from tourney.forms import RegisterForm, ProfileForm


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

    context['player'] = player
    context['ppd_casual'] = casual_stat['PPD']
    context['mpr_casual'] = casual_stat['MPR']
    context['ppd_ranking'] = ranking_stat['PPD']
    context['mpr_ranking'] = ranking_stat['MPR']
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


def _get_card_info(rfid):
    cursor = connections['hi'].cursor()
    cursor.execute("""SELECT a.name, b.rfid, b.utime FROM userinfo a
        RIGHT JOIN checkrfid b ON a.rfid= b.rfid
        WHERE b.rfid=%s""", [rfid])
    r = cursor.fetchone()
    return r


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


def card(request, rfid_id):
    # check card valid
    context = dict()
    card_info = _get_card_info(rfid_id)

    if not card_info:
        msg = 'invalid card no'
    else:
        [name, rfid, utime] = list(card_info)

        if rfid and utime and name:
            msg = 'signed up card'
        elif name and not utime:
            msg = 'temp card'
        else:
            msg = 'blank card'

        try:
            player = Player.objects.get(rfid=rfid_id)
            msg = 'tournament card'
            context['player'] = player
        except Player.DoesNotExist:
            pass
    # if _is_new_card(rfid_id):
    #     msg = 'new card'
    # else:
    #     try:
    #         player = Player.objects.get(rfid=rfid_id)
    #         msg = 'tournament card'
    #         context['player'] = player
    #     except Player.DoesNotExist:
    #         msg = 'casual card'

    context['msg'] = msg
    return render(request, 'tourney/card.html', context)
