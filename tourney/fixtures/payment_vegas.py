#!/usr/bin/env python

import sys
from decimal import Decimal
sys.path.append('/home/sopae/djangostack-1.4.5-0/apps/django/django_projects/helio')
sys.path.append('/Applications/djangostack-1.4.6-0/apps/django/django_projects/helio')
sys.path.append('/Applications/djangostack-1.4.5-0/apps/django/django_projects/helio')

from csv import reader
from helio.settings import local, production
from django.core.management import setup_environ
setup_environ(local)
# setup_environ(production)
from tourney.models import PreRegVegas, Player, Card, Entry, Tournament, SignupPayment
from tourney.phoenixcard import PhoenixCard, PhoenixLeagueCard
from decimal import Decimal

counter = {'22k': 0, 'casual_invalid': 0, 'league_invalid': 0}

vegas_tourney = Tournament.objects.get(id=5)

for no, reg in enumerate(PreRegVegas.objects.all(), start=1):
    if reg.player_id:
        # entry = Entry.objects.get(tournament=vegas_tourney, player_id=reg.player_id)
        if reg.fri_singles:
            SignupPayment.objects.get_or_create(player_id=reg.player_id, event_id=29, paid=True)
            SignupPayment.objects.get_or_create(player_id=reg.player_id, event_id=30, paid=True)
            # print reg.first_name
        if reg.sat_doubles:
            SignupPayment.objects.get_or_create(player_id=reg.player_id, event_id=33, paid=True)
            SignupPayment.objects.get_or_create(player_id=reg.player_id, event_id=34, paid=True)
        if reg.sat_triples:
            SignupPayment.objects.get_or_create(player_id=reg.player_id, event_id=37, paid=True)
        if reg.sun_doubles:
            SignupPayment.objects.get_or_create(player_id=reg.player_id, event_id=39, paid=True)
            SignupPayment.objects.get_or_create(player_id=reg.player_id, event_id=40, paid=True)
        print no, reg.first_name, ' => done'