#!/usr/bin/env python
import sys
import re

pk = 1

# print """- model: tourney.Tournament
#   pk: 1
#   fields:
#     title: Lansdale, PA
#     start_at: 2013-01-25 17:00
#     end_at: 2013-01-27 17:00
# - model: tourney.Tournament
#   pk: 2
#   fields:
#     title: Pittsburgh, PA
#     start_at: 2013-03-29 17:00
#     end_at: 2013-03-31 17:00

# """

while 1:
    try:
        line = sys.stdin.readline().rstrip('\n')
    except KeyboardInterrupt:
        break

    if not line:
        break

    fields = [field.strip() for field in line.split(',')]
    if(len(fields) < 8):
        print "%s: %s -> skip" % (pk, line)
        continue

    rfid = ''
    cardno = ''
    first_name = 'N/A'
    last_name = 'N/A'
    gender = ''
    email = ''
    phone = ''
    city = ''
    state = ''
    street_line1 = ''
    zipcode = ''

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

    gender = 'M' if fields[1].title() == 'Male' else 'F'
    email = fields[2].strip().lower()
    phone = re.sub('[()-]', '', fields[3].strip().replace(' ', ''))
    city = fields[4].strip().title()
    state = fields[5].strip().upper()
    street_line1 = fields[6].strip().title()
    zipcode = fields[7].strip()

    print """- model: tourney.Player2
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
