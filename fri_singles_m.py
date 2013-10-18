from tourney.models import *

teams = Team.objects.filter(event_id=29)

for no, team in enumerate(teams, start=1):
	p = team.players.all()[0]
	c_stats = p.casual_stat()
	print no, p, c_stats['MPR'], c_stats['PPD']