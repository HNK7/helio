from django.contrib import admin
from tourney.models import Tournament, Event, Player, Team, Entry

admin.site.register(Tournament)
admin.site.register(Event)
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Entry)
