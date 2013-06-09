from django import template

register = template.Library()


@register.filter(name='format_phone_number')
def format_phone_number(number):
    return '(%s%s%s) %s%s%s-%s%s%s%s' % tuple(number)


@register.filter(name='format_card_number')
def format_card_number(number):
    return '%s%s%s%s %s%s%s%s %s%s%s%s %s%s%s%s' % tuple(number)


@register.filter(name='players_in_team')
def players_in_team(team):
    return ', '.join(map(str, team.players.all()))


@register.filter(name='num_teams')
def num_teams(event):
    teams = event.team_set.all().exclude(name__isnull=True)
    return teams.count()


@register.filter(name='num_players')
def num_players(event):
    teams = event.team_set.all()
    return sum(team.players.count() for team in teams)
