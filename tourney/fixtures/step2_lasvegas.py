#!/usr/bin/env python

import sys
sys.path.append('/home/sopae/djangostack-1.4.5-0/apps/django/django_projects/helio')
sys.path.append('/Applications/djangostack-1.4.6-0/apps/django/django_projects/helio')
sys.path.append('/Applications/djangostack-1.4.5-0/apps/django/django_projects/helio')

from csv import reader
from helio.settings import local 
from django.core.management import setup_environ
setup_environ(local)
from tourney.models import PreRegVegas, Player, Card

total_reg = PreRegVegas.objects.count()
print "-------------------------"
print "Total: %s" % total_reg
print "-------------------------"

for no, reg in enumerate(PreRegVegas.objects.all(), start=1):
    result = ''
    if not Card(cardno=reg.casual_card).is_cardno_valid():
        result += 'invalid casual card'
    
    result = 'ok' if result == '' else result
    print '%s: %s => %s' % (no, reg, result)
