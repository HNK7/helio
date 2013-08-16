from django import template
import locale

register = template.Library()


@register.filter(name='format_phone_number')
def format_phone_number(number):
    number = ''.join(e for e in number if e.isalnum())
    return '(%s%s%s) %s%s%s-%s%s%s%s' % tuple(number) if len(number) == 10 else number


@register.filter(name='format_card_number')
def format_card_number(number):
    return '%s%s%s%s %s%s%s%s %s%s%s%s %s%s%s%s' % tuple(number) if len(number) == 16 else number


@register.filter(name='players_in_team')
def players_in_team(team):
    return ', '.join(map(str, team.players.all()))


@register.filter(name='num_teams')
def num_teams(event):
    teams = event.team_set.all().exclude(name__isnull=True)
    return teams.count()


@register.filter(name='num_players')
def num_players(event):
    if event.draw == 'L':
        return event.drawentry_set.all().count()
    else:
        teams = event.team_set.all()
        return sum(team.players.count() for team in teams)


@register.filter(name='entry_stat_team')
def entry_stat_team(team, mode='team'):
    tourney = team.event.tournament
    if mode == 'team':
        team_stat = team.mpr_rank if (team.event.game == 'CR' or team.event.game == 'Medley') else team.ppd_rank
        return '%s' % (team_stat)
    else:
        players = team.players.all()
        players_stat = []
        for player in players:
            if team.event.game == 'CR' or team.event.game == 'Medley':
                player_stat = player.entry_set.filter(tournament=tourney)[0].mpr_rank
            elif team.event.game == '501' or team.event.game == '701':
                player_stat = player.entry_set.filter(tournament=tourney)[0].ppd_rank
            players_stat.append(str(player_stat))
        return '%s' % (', '.join(players_stat))
    


@register.filter(name='entry_stat_player')
def entry_stat_player(drawentry):
    tourney = drawentry.event.tournament
    if drawentry.event.game == 'CR' or drawentry.event.game == 'Medley':
        player_stat = drawentry.player.entry_set.filter(tournament=tourney)[0].mpr_rank
    elif drawentry.event.game == '501' or drawentry.event.game == '701':
        player_stat = drawentry.player.entry_set.filter(tournament=tourney)[0].ppd_rank
    else:
        player_stat = 0
    return player_stat


@register.filter(name='currency')
def currency(value):
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        locale.setlocale(locale.LC_ALL, '')
    loc = locale.localeconv()
    return locale.currency(value, loc['currency_symbol'], grouping=True)


@register.filter
def get_range(stop, start=0):
    return range(start, stop)


@register.filter
def get_bid(player_pos, i):
    return player_pos[i] if player_pos[i] else ''

