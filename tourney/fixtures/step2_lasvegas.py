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
from tourney.models import PreRegVegas, Player, Card, Entry, Tournament
from tourney.phoenixcard import PhoenixCard
from decimal import Decimal

counter = {'22k': 0, 'casual_invalid': 0, 'league_invalid': 0}

vegas_tourney = Tournament.objects.get(id=5)

for no, reg in enumerate(PreRegVegas.objects.all(), start=1):

    line = str(no) + ': ' + ' '.join([reg.first_name, reg.last_name])
    if reg.casual_card:
        pxcard = PhoenixCard(cardno=reg.casual_card)
        # pxcard = PhoenixCard(cardno=1223)
        try:
            rfid = pxcard.get_rfid()
            # org_rfid = pxcard.get_org_rfid()
        except Exception, e:
            print line, e
            counter['casual_invalid'] += 1
            continue
        try:
            card = Card.objects.get(cardno=pxcard.cardno)
            # Card.objects.get(rfid=org_rfid)
            print line, 'already registered'
            counter['22k'] += 1
            entry, created = Entry.objects.get_or_create(tournament=vegas_tourney, player=card.player)
            if reg.balance > 0:
                entry.balance_signup = Decimal(entry.balance_signup) + Decimal(reg.balance)

            entry.qualified = True
            entry.save()
            print  entry
        except Card.DoesNotExist:
            print line, 'new player'


print 'Total: %s' % no
print '22k Member: %s' % counter['22k']
print 'invalid casual: %s' % counter['casual_invalid']
print 'invalid league: %s' % counter['league_invalid']