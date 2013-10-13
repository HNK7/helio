#!/usr/bin/env python

import sys
sys.path.append('/home/sopae/djangostack-1.4.5-0/apps/django/django_projects/helio')
sys.path.append('/Applications/djangostack-1.4.6-0/apps/django/django_projects/helio')
from csv import reader
from helio import settings
from django.core.management import setup_environ
setup_environ(settings)
from tourney.models import PreRegVegas


def register(item):
    (Payment, Operator, First_Name, Last_Name, Mobile, Email, Adress, Casual_Card, League_Card,
      Fri_Singles, Sat_Doubles, Sat_Triples, Sun_Doubles, Package_Purchased, Paid_Amount, Balance, CR_Partner, Zero_Parter, Note ) = item

    # Amount = ''.join(e for e in Amount if e.isalnum())

    if Casual_Card:
      cn  = ''.join(Casual_Card.strip().split())
      print '%s%s%s%s %s%s%s%s %s%s%s%s %s%s%s%s' % tuple(cn), cn
    # print First_Name, Last_Name, Email, Phone, Zip, Amount, Note
    # pre_reg = PreRegPlayer.objects.create(first_name=First_Name.title(),
    #                                last_name=Last_Name.title(),
    #                                email=Email.lower(),
    #                                phone=Phone,
    #                                zipcode=Zip,
    #                                credit=Amount,
    #                                note=Note)
    # pre_reg = PreRegPlayer(first_name=First_Name.title(),
    #                                last_name=Last_Name.title(),
    #                                email=Email.lower(),
    #                                phone=Phone,
    #                                zipcode=Zip,
    #                                credit=Amount,
    #                                note=Note)
    # print "=> %s" % (pre_reg)
    # card.save()
    # entry = Entry(tournament=tourney, player=player)
    # entry.save()

with open('prepay_lasvegas.csv') as f:
    reader = reader(f)
    for row in reader:
      register(row)