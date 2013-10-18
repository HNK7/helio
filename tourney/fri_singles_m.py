from tourney.models import *

teams = Team.objects.filter(event_id=29)

for no, team in enumerate(team):
	print team.name