from tourney.models import *
from django.db import connections, transaction


def update_stat(mpr, ppd, rfid):
    cursor = connections['hi'].cursor()
    cursor.execute("UPDATE useravg SET mpr_ta2=%s, ppd_ta2=%s WHERE rfid = getorigrfid2(%s)", [mpr, ppd, rfid])
    transaction.commit_unless_managed(using='hi')# teams = Team.objects.filter(event_id=29)

teams = Team.objects.filter(event_id=29)
for no, team in enumerate(teams, start=1):
	p = team.players.all()[0]
	c_stats = p.casual_stat()
	entry = p.entry_set.all()[0]

	if c_stats['MPR'] < entry.mpr_event or c_stats['PPD'] < entry.ppd_event:
		print no, p, ' update casual stat'
		update_stat(entry.mpr_event, entry.ppd_event, p.card.rfid)
	else:
		print no, p, ' ok'
	# print no, p, c_stats['MPR'], c_stats['PPD'], entry.mpr_event, entry.ppd_event