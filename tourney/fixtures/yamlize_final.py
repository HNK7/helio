#!/usr/bin/env python
import sys
import re

pk = 1

print """- model: tourney.Tournament
  pk: 1
  fields:
    title: Lansdale, PA
    start_at: 2013-01-25 17:00
    end_at: 2013-01-27 17:00
- model: tourney.Tournament
  pk: 2
  fields:
    title: Pittsburgh, PA
    start_at: 2013-03-29 17:00
    end_at: 2013-03-31 17:00

"""

while 1:
    try:
        line = sys.stdin.readline().rstrip('\n')
    except KeyboardInterrupt:
        break

    if not line:
        break

    fields = [field.strip() for field in line.split(',')]
    if(len(fields) < 5):
        print "%s: %s -> skip" % (pk, line)
        continue

    rfid = ''
    cardno = ''
    first_name = ''
    last_name = ''
    gender = ''
    email = ''
    phone = ''
    city = ''
    state = ''
    street_line1 = ''
    zipcode = ''

    rfid = fields[1].strip()
    cardno = fields[3].strip()
    names = [field.strip().title() for field in fields[0].split()]
    if(len(names) == 3):
        # ignaore middle name
        first_name = names[0]
        last_name = names[2]
    elif(len(names) == 1):
        # no last name
        first_name = names[0]
    elif(len(names) == 2):
        first_name = names[0]
        last_name = names[1]

    # gender = 'M' if fields[2].title() == 'Male' else 'F'
    # email = fields[3].strip().lower()
    phone = re.sub('[()-]', '', fields[4].strip().replace(' ', ''))
    # street_line1 = fields[5].strip().title()
    # city = fields[6].strip().title()
    # zipcode = fields[7].strip()
    # state = fields[8].strip().upper()

    print """- model: tourney.Player
  pk: %s
  fields:
    rfid: %s
    cardno: %s
    first_name: %s
    last_name: %s
    gender: %s
    email: %s
    phone: %s
    city: %s
    state: %s
    street_line1: %s
    zipcode: %s

""" % (pk, rfid, cardno, first_name, last_name, gender, email, phone, city, state, street_line1, zipcode)
    pk += 1
