#!/usr/bin/env python

import sys
sys.path.append('/Applications/djangostack-1.4.5-0/apps/django/django_projects/helio')

from helio import settings
from django.core.management import setup_environ
setup_environ(settings)

from tourney.models import Tournament, Entry, Event, Card, Player, DrawEntry
from random import choice

mprs = [2.1, 3.0, 1.7, 2.4, 4.27, 3.65, 2.0, 1.39, 3.95, 2.45, 4.0, 3.1]
ppds = [12, 29.5, 37.5, 40.5, 19.5, 34.95, 27.4, 11.3, 50.6, 19.4, 18.0]

for i in range(1, 128):
    tourney = Tournament.objects.get(id=3)
    event = Event.objects.get(id=2)
    player = Player.objects.create(first_name='player_%s' % [i],
                    last_name='',
                    gender='M',
                    email='mail@mail.com',
                    phone='213-111-1111')
    Card.objects.create(cardno='%s' % [i], rfid='%s' % [i], player=player)

    Entry.objects.create(tournament=tourney,
                          player=player,
                          mpr_rank=choice(mprs),
                          ppd_rank=choice(ppds))
    DrawEntry.objects.create(event=event, player=player)
