#!/usr/bin/env python

import sys
sys.path.append('/home/sopae/djangostack-1.4.5-0/apps/django/django_projects/helio')
sys.path.append('/Applications/djangostack-1.4.6-0/apps/django/django_projects/helio')
sys.path.append('/Applications/djangostack-1.4.5-0/apps/django/django_projects/helio')

from csv import reader
from helio import settings
from django.core.management import setup_environ
setup_environ(settings)
from tourney.models import PreRegVegas


class PhoenixCard(object):
    """RFID card for playing phoniex dart machine"""
    def __init__(self, number, rfid=None):
        super(PhoenixCard, self).__init__()
        self.number = number
        self.rifd = rfid

    def __str__(self):
        return '%s%s%s%s %s%s%s%s %s%s%s%s %s%s%s%s' % tuple(self.number)

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, n):
        # clean up card number
        c_n = ''.join(n.strip().split())
        if not c_n.isdigit() or len(c_n) != 16:
            raise Exception("Invalid Phoenix Card Number: %s" % (n))
        self._number = c_n

def register(item, line_no):
    cleaned_item = map(str.strip, item)
    (Payment, Operator, First_Name, Last_Name, Mobile, Email, Adress, Casual_Card, League_Card,
      Fri_Singles, Sat_Doubles, Sat_Triples, Sun_Doubles, Package_Purchased,
      Paid_Amount, Balance, CR_Partner, Zero_Parter, Note ) = cleaned_item

    # Amount = ''.join(e for e in Amount if e.isalnum())

    # Strip
    line_number = '%s: ' % line_no
    first_name = First_Name.title()
    last_name = Last_Name.title()
    mobile = Mobile
    # cn  = ''.join(Casual_Card.split())
    # ln  = ''.join(League_Card.split())
    # c_number = '%s%s%s%s %s%s%s%s %s%s%s%s %s%s%s%s' % tuple(cn) if len(cn) == 16 else 'invalid'
    # l_number = '%s%s%s%s %s%s%s%s %s%s%s%s %s%s%s%s' % tuple(ln) if len(ln) == 16 else 'invalid'
    c_card = PhoenixCard(number=Casual_Card)
    l_card = PhoenixCard(number=League_Card)
    # print line_number, first_name, last_name, c_number, cn, l_number, ln
    print line_number, first_name, last_name, c_card, l_card
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
    line_no = 1
    for row in reader:
      register(row, line_no)
      line_no += 1