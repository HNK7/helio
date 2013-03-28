#!/usr/bin/env python

import sys
sys.path.append('/Applications/djangostack-1.4.5-0/apps/django/django_projects/helio')

from helio import settings
from django.core.management import setup_environ
setup_environ(settings)

from tourney.models import Ranking


while 1:
    try:
        line = sys.stdin.readline().rstrip('\n')
    except KeyboardInterrupt:
        break

    if not line:
        break

    fields = [field.strip() for field in line.split(',')]
    userid = fields[0].strip()
    ppd = fields[1].strip()
    mpr = fields[2].strip()

    try:
        ranking = Ranking.objects.get(pk=userid)
        #ranking already exits

    except Ranking.DoesNotExist:
        ranking = Ranking(userid=userid)

    if ppd:
            ranking.ppd = ppd
    if mpr:
            ranking.mpr = mpr
    ranking.save()
