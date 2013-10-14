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
from tourney.models import PreRegVegas, Player, Card, Entry

counter = {'22k': 0, 'casual_invalid': 0, 'league_invalid': 0}

for no, reg in enumerate(PreRegVegas.objects.all(), start=1):
    result = []
    # Check casual card
    if reg.casual_card:
  # #   	player_22k = reg.get_22k_member()
  # #   	if player_22k:
	 # #    	result.append('22k')
	 # #    	counter['22k'] += 1

    	c_stat = Card().casual_stat(cardno=reg.casual_card)
    	if c_stat:
	    	# result.append('casual: %s' % casual_stat)
	  #   	cs_stat['PPD'] = c_stat['PPD']
			# cs_stat['MPR'] = c_stat['MPR']
			pass
		else:
	        result.append('casual: invalid')
	        counter['casual_invalid'] += 1
    else:
    	result.append('no casual card')
	    
	# Check league card
   #  if reg.league_card:
	  #   l_stat = Card().league_stat(cardno=reg.league_card)
	  #   if l_stat['PPD'] or l_stat['MPR']:
	  #   	# result.append('league: %s' % league_stat)
	  #   	lg_stat['PPD'] = l_stat['PPD']
	  #   	lg_stat['MPR'] = l_stat['MPR']
	  #   else:
			# result.append('league: invalid card')
			# counter['league_invalid'] += 1
   #  else:
   #  	result.append('league: no card')

	ppd_diff = cs_stat['PPD'] - lg_stat['PPD']
	mpr_diff = cs_stat['MPR'] - lg_stat['MPR']
	result.append('ppd/mpr diff: %s / %s' % [ppd_diff, mpr_diff])
	result.append('ok')
    print '%s: %s => %s' % (no, reg, ', '.join(result))

print 'Total: %s' % no
print '22k Member: %s' % counter['22k']
print 'invalid casual: %s' % counter['casual_invalid']
print 'invalid league: %s' % counter['league_invalid']