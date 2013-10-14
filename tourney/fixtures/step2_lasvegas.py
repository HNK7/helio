#!/usr/bin/env python

import sys
from decimal import Decimal
sys.path.append('/home/sopae/djangostack-1.4.5-0/apps/django/django_projects/helio')
sys.path.append('/Applications/djangostack-1.4.6-0/apps/django/django_projects/helio')
sys.path.append('/Applications/djangostack-1.4.5-0/apps/django/django_projects/helio')

from csv import reader
from helio.settings import local 
from django.core.management import setup_environ
setup_environ(local)
from tourney.models import PhoenixCard, PreRegVegas, Player, Card, Entry

counter = {'22k': 0, 'casual_invalid': 0, 'league_invalid': 0}

for no, reg in enumerate(PreRegVegas.objects.all(), start=1):
    if reg.casual_card:
        try:
            card = PhoenixCard(cardno=reg.casual_card)
            card.rfid = card.get_rfid()
            stat = card.get_stat()
            print no, reg.first_name, reg.last_name, card.cardno, stat['PPD'], stat['MPR']
        except:
            print no, reg.first_name, reg.last_name, "invalid casual number"
            pass
    else:
        print no, reg.first_name, reg.last_name, "no casual card"

print 'Total: %s' % no
print '22k Member: %s' % counter['22k']
print 'invalid casual: %s' % counter['casual_invalid']
print 'invalid league: %s' % counter['league_invalid']