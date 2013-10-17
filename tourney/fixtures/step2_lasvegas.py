#!/usr/bin/env python

import sys
from decimal import Decimal
sys.path.append('/home/sopae/djangostack-1.4.5-0/apps/django/django_projects/helio')
sys.path.append('/Applications/djangostack-1.4.6-0/apps/django/django_projects/helio')
sys.path.append('/Applications/djangostack-1.4.5-0/apps/django/django_projects/helio')

from csv import reader
from helio.settings import local, production
from django.core.management import setup_environ
setup_environ(production)
# setup_environ(production)
from tourney.models import PreRegVegas, Player, Card, Entry, Tournament
from tourney.phoenixcard import PhoenixCard, PhoenixLeagueCard
from decimal import Decimal

counter = {'22k': 0, 'casual_invalid': 0, 'league_invalid': 0}

vegas_tourney = Tournament.objects.get(id=5)

for no, reg in enumerate(PreRegVegas.objects.all(), start=1):

    line = str(no) + ': ' + ' '.join([reg.first_name, reg.last_name])
    if reg.casual_card and reg.league_card:

        try:
            pxcard = PhoenixCard(cardno=reg.casual_card)
            plcard = PhoenixLeagueCard(cardno=reg.league_card)
        except Exception, e:
            pass
            print line, e
            continue
        ppd_diff = pxcard.ppd - plcard.ppd
        mpr_diff = pxcard.mpr - plcard.mpr
        # print line, pxcard.ppd, pxcard.mpr, ppd_diff, mpr_diff

        # Create/Update card and player
        try:
            card = Card.objects.get(cardno=pxcard.cardno)
            player = card.player
            player.first_name = reg.first_name
            player.last_name = reg.last_name
            player.save()
            print 'Updated already registered player'
        except Exception, e:
            player = Player.objects.create(first_name=reg.first_name, last_name=reg.last_name)
            player.gender = reg.gender
            player.email = reg.email if reg.email else ''
            player.phone = reg.mobile if reg.mobile else ''
            player.save()
            card = Card.objects.create(cardno=pxcard.cardno, rfid=pxcard.rfid, player=player)
            print 'Registered as a new player'
            print 'player id: %s' % player.id
            print 'card id: %s' % card.id
            # pass
            # print line, 'skipped: New player'
            # continue

        # Mark Prereg player
        reg.player_id = player.id
        reg.save()
        # Register for 100K
        entry, created = Entry.objects.get_or_create(tournament=vegas_tourney, player=player)
        if reg.balance > 0:
            entry.balance_signup = Decimal(entry.balance_signup) + Decimal(reg.balance)

        entry.mpr_rank = pxcard.mpr
        entry.ppd_rank = pxcard.ppd
        entry.mpr_event = plcard.mpr
        entry.ppd_event = plcard.ppd
        entry.qualified = True
        entry.save()
        print line, entry

    else:
        print line, 'skppied: no casual card or league card'
    # (card_type, rfid, cardno, old_cardno, old_rfid, userinfo_rfid, members_rfid, name,
    # m_num, utime, f_name, l_name, m_sex, m_email, m_phone, m_id, m_zip, ppd, mpr) = pxcard.get_card_info()

    # if reg.casual_card:
    #     pxcard = PhoenixCard(cardno=reg.casual_card)
    #     # pxcard = PhoenixCard(cardno=1223)
    #     try:
    #         rfid = pxcard.get_rfid()
    #         # org_rfid = pxcard.get_org_rfid()
    #     except Exception, e:
    #         print line, e
    #         counter['casual_invalid'] += 1
    #         continue
    #     try:
    #         card = Card.objects.get(cardno=pxcard.cardno)
    #         # Card.objects.get(rfid=org_rfid)
    #         print line, 'already registered'
    #         counter['22k'] += 1
    #         entry, created = Entry.objects.get_or_create(tournament=vegas_tourney, player=card.player)
    #         if reg.balance > 0:
    #             entry.balance_signup = Decimal(entry.balance_signup) + Decimal(reg.balance)

    #         entry.qualified = True
    #         entry.save()
    #         print  entry
    #     except Card.DoesNotExist:
    #         print line, 'new player'


print 'Total: %s' % no
print '22k Member: %s' % counter['22k']
print 'invalid casual: %s' % counter['casual_invalid']
print 'invalid league: %s' % counter['league_invalid']