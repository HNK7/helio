#!/usr/bin/env python

import sys
sys.path.append('/home/sopae/djangostack-1.4.5-0/apps/django/django_projects/helio')
sys.path.append('/Applications/djangostack-1.4.6-0/apps/django/django_projects/helio')
sys.path.append('/Applications/djangostack-1.4.5-0/apps/django/django_projects/helio')

from csv import reader
from helio.settings import production 
from django.core.management import setup_environ
setup_environ(production)
from tourney.models import PreRegVegas


class PhoenixCard(object):
    """RFID card for playing phoniex dart machine"""
    def __init__(self, number, rfid=None):
        super(PhoenixCard, self).__init__()
        self.number = number
        self.rifd = rfid

    def __str__(self):
        return '%s%s%s%s %s%s%s%s %s%s%s%s %s%s%s%s' % tuple(self.number)


def register(item, line_no):
    cleaned_item = map(str.strip, item)
    (Payment, Operator, First_Name, Last_Name, Gender, Mobile, Email, Address, Casual_Card, League_Card,
      Fri_Singles, Sat_Doubles, Sat_Triples, Sun_Doubles, Package_Purchased,
      Paid_Amount, Balance, CR_Partner, Zero_Parter, Note ) = cleaned_item

    # Amount = ''.join(e for e in Amount if e.isalnum())

    # Strip
    line_number = '%s: ' % line_no
    first_name = First_Name.title()
    last_name = Last_Name.title()
    cn  = ''.join(Casual_Card.split())
    ln  = ''.join(League_Card.split())
    c_number = '%s%s%s%s %s%s%s%s %s%s%s%s %s%s%s%s' % tuple(cn) if len(cn) == 16 else 'invalid'
    l_number = '%s%s%s%s %s%s%s%s %s%s%s%s %s%s%s%s' % tuple(ln) if len(ln) == 16 else 'invalid'
    fri_singles = True if Fri_Singles == 'yes' else False
    sat_doubles = True if Sat_Doubles == 'yes' else False
    sat_triples = True if Sat_Triples == 'yes' else False
    sun_doubles = True if Sun_Doubles == 'yes' else False
    credit = Paid_Amount.replace('$', '') if Paid_Amount else 0
    if Balance == 'PAID':
        balance = 0
    else:
        balance = Balance.replace('$', '') if Balance else 0
    
    # print line_number, first_name, last_name, c_number, cn, l_number, ln
    
    pre_player = PreRegVegas.objects.create(first_name=first_name,
        last_name=last_name,
        gender=Gender,
        mobile=Mobile,
        email=Email.lower(),
        casual_card=cn,
        league_card=ln,
        fri_singles=fri_singles,
        sat_doubles=sat_doubles,
        sat_triples=sat_triples,
        sun_doubles=sun_doubles,
        package=Package_Purchased,
        credit=credit,
        balance=balance,
        partner_cricket=CR_Partner,
        partner_01=Zero_Parter,
        note=Note)
    print "%s => %s" % (line_number, pre_player)
    # card.save()
    # entry = Entry(tournament=tourney, player=player)
    # entry.save()

with open('prepay_lasvegas.csv') as f:
    reader = reader(f)
    line_no = 1
    for row in reader:
        register(row, line_no)
        line_no += 1