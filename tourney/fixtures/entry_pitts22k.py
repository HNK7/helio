#!/usr/bin/env python

import sys
sys.path.append('/Applications/djangostack-1.4.5-0/apps/django/django_projects/helio')

from helio import settings
from django.core.management import setup_environ
setup_environ(settings)

from tourney.models import Card, Tournament, Player, Entry
from django.db import connections


def get_rfid(cardno):
    cursor = connections['hi'].cursor()
    cursor.execute("SELECT rfid FROM checkrfid WHERE cardno=%s", [cardno])
    r = cursor.fetchone()
    return r[0] if r[0] else None


def register(item):
    if len(item) < 4:
        print "missing info: %s => skipped" % item
    (first_name, last_name, gender, cardno) = item

    tourney = Tournament.objects.get(id=2)
    player = Player.objects.create(first_name=first_name.title(),
                                   last_name=last_name.title(),
                                   gender=gender)

    card = Card.objects.create(cardno=cardno, rfid=get_rfid(cardno), player=player)
    Entry.objects.create(tournament=tourney, player=player)
    print "%s registered => %s" % (player, card)
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

    try:
        register(line.split(','))
    except:
        break
