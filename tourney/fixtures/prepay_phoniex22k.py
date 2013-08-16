#!/usr/bin/env python

import sys
sys.path.append('/home/sopae/djangostack-1.4.5-0/apps/django/django_projects/helio')

from helio import settings
from django.core.management import setup_environ
setup_environ(settings)

from tourney.models import PreRegPlayer


def register(item):
    (First_Name, Last_Name, Email, Phone, Zip, Amount, Note) = item

    Amount = ''.join(e for e in Amount if e.isalnum())

    print First_Name, Last_Name, Email, Phone, Zip, Amount, Note
    pre_reg = PreRegPlayer.objects.create(first_name=First_Name.title(),
                                   last_name=Last_Name.title(),
                                   email=Email.lower(),
                                   phone=Phone,
                                   zipcode=Zip,
                                   credit=Amount,
                                   note=Note)
    # pre_reg = PreRegPlayer(first_name=First_Name.title(),
    #                                last_name=Last_Name.title(),
    #                                email=Email.lower(),
    #                                phone=Phone,
    #                                zipcode=Zip,
    #                                credit=Amount,
    #                                note=Note)
    print "=> %s" % (pre_reg)
    # card.save()
    # entry = Entry(tournament=tourney, player=player)
    # entry.save()


while 1:
    try:
        line = sys.stdin.readline().rstrip('\n')
    except KeyboardInterrupt:
        break

    if not line:
        break

        line_item = line.split(',')

    register(line.split(','))
