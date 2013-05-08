#!/usr/bin/env python

import gdata.spreadsheet.service

gd_client = gdata.spreadsheet.service.SpreadsheetsService()
gd_client.email = 'phoenix@dartoo.com'
gd_client.password = '3355dartoO'
gd_client.source = '22K'
gd_client.ProgrammaticLogin()
spreadsheet_key = 'tVc9gCzhh-seVwvaojke4Iw'
feed = gd_client.GetWorksheetsFeed(spreadsheet_key)
worksheet_id = 'od6'
for entry in feed.entry:
    if entry.title.text == 'Entry':
        worksheet_id = entry.id.text.rsplit('/', 1)[1]

row = {}
row['sex'] = 'm'
row['name'] = 'stu'
row['mobile'] = '2134223214'
row['mpr'] = '3.4'
row['ppd'] = '34.24'
row['cardno'] = '12432155533'
row['entry'] = '$15'  # if he is not member else '$0'
row['card'] = '$5'  # if he has not his card else '$0'

entry = gd_client.InsertRow(row, spreadsheet_key, worksheet_id)
if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
    print "succeed"
else:
    print "failed"
