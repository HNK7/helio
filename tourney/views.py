from django.db import connections
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from tourney.models import Tournament, Player
from tourney.forms import RegisterForm


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
    context['player'] = Player.objects.get(id=p_id)
    return render(request, 'tourney/profile.html', context)


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


def is_blank_card(rfid):
    cursor = connections['hi'].cursor()
    cursor.execute("SELECT utime FROM checkrfid where rfid = %s", [rfid])
    r = cursor.fetchone()
    return True if not r else False


def card(request, rfid_id):
    # check card valid
    context = dict()
    if is_blank_card(rfid_id):
        msg = 'blank card'
    else:
        try:
            player = Player.objects.get(rfid=rfid_id)
            msg = 'tournament card'
            context['player'] = player
        except Player.DoesNotExist:
            msg = 'casual card'

    context['msg'] = msg
    return render(request, 'tourney/card.html', context)
