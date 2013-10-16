#!/usr/bin/env python

import sys
from decimal import Decimal
sys.path.append('/home/sopae/djangostack-1.4.5-0/apps/django/django_projects/helio')
# sys.path.append('/Applications/djangostack-1.4.6-0/apps/django/django_projects/helio')
# sys.path.append('/Applications/djangostack-1.4.5-0/apps/django/django_projects/helio')

from csv import reader
from helio.settings import local, production
from django.core.management import setup_environ
setup_environ(production)
from tourney.models import PreRegVegas, Player, Card, Entry
from tourney.pheonixcard import PhoenixCard

counter = {'22k': 0, 'casual_invalid': 0, 'league_invalid': 0}

for no, reg in enumerate(PreRegVegas.objects.all(), start=1):

    line = ' '.join([str(no), ':']) + ' '.join([reg.first_name, reg.last_name])
    if reg.casual_card:
        pxcard = PhoenixCard(cardno=reg.casual_card)
        try:
            pxcard.get_rfid()
        except Exception, e:
            print line, e
            continue
        try:
            Card.objects.get(cardno=pxcard.cardno)
            print line, 'already registered'
        except Card.DoesNotExist:
            print line, 'new player'


print 'Total: %s' % no
print '22k Member: %s' % counter['22k']
print 'invalid casual: %s' % counter['casual_invalid']
print 'invalid league: %s' % counter['league_invalid']