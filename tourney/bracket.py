#!/usr/bin/python


matches = [ {'teams':[], 'ranking': None, 'losers_go': None, 'winners_go': None, 'id': 0, 'round': 0},
    {'teams':[], 'ranking': None, 'losers_go': 64, 'winners_go': 33, 'id': 1, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 64, 'winners_go': 33, 'id': 2, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 65, 'winners_go': 34, 'id': 3, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 65, 'winners_go': 34, 'id': 4, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 66, 'winners_go': 35, 'id': 5, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 66, 'winners_go': 35, 'id': 6, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 67, 'winners_go': 36, 'id': 7, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 67, 'winners_go': 36, 'id': 8, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 68, 'winners_go': 37, 'id': 9, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 68, 'winners_go': 37, 'id': 10, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 69, 'winners_go': 38, 'id': 11, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 69, 'winners_go': 38, 'id': 12, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 70, 'winners_go': 39, 'id': 13, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 70, 'winners_go': 39, 'id': 14, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 71, 'winners_go': 40, 'id': 15, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 71, 'winners_go': 40, 'id': 16, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 72, 'winners_go': 41, 'id': 17, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 72, 'winners_go': 41, 'id': 18, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 73, 'winners_go': 42, 'id': 19, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 73, 'winners_go': 42, 'id': 20, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 74, 'winners_go': 43, 'id': 21, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 74, 'winners_go': 43, 'id': 22, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 75, 'winners_go': 44, 'id': 23, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 75, 'winners_go': 44, 'id': 24, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 76, 'winners_go': 45, 'id': 25, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 76, 'winners_go': 45, 'id': 26, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 77, 'winners_go': 46, 'id': 27, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 77, 'winners_go': 46, 'id': 28, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 78, 'winners_go': 47, 'id': 29, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 78, 'winners_go': 47, 'id': 30, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 79, 'winners_go': 48, 'id': 31, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 79, 'winners_go': 48, 'id': 32, 'round': 1},
    {'teams':[], 'ranking': None, 'losers_go': 81, 'winners_go': 49, 'id': 33, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 80, 'winners_go': 49, 'id': 34, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 83, 'winners_go': 50, 'id': 35, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 82, 'winners_go': 50, 'id': 36, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 85, 'winners_go': 51, 'id': 37, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 84, 'winners_go': 51, 'id': 38, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 87, 'winners_go': 52, 'id': 39, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 86, 'winners_go': 52, 'id': 40, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 89, 'winners_go': 53, 'id': 41, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 88, 'winners_go': 53, 'id': 42, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 91, 'winners_go': 54, 'id': 43, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 90, 'winners_go': 54, 'id': 44, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 93, 'winners_go': 55, 'id': 45, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 92, 'winners_go': 55, 'id': 46, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 95, 'winners_go': 56, 'id': 47, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 94, 'winners_go': 56, 'id': 48, 'round': 2},
    {'teams':[], 'ranking': None, 'losers_go': 105, 'winners_go': 57, 'id': 49, 'round': 3},
    {'teams':[], 'ranking': None, 'losers_go': 104, 'winners_go': 57, 'id': 50, 'round': 3},
    {'teams':[], 'ranking': None, 'losers_go': 107, 'winners_go': 58, 'id': 51, 'round': 3},
    {'teams':[], 'ranking': None, 'losers_go': 106, 'winners_go': 58, 'id': 52, 'round': 3},
    {'teams':[], 'ranking': None, 'losers_go': 109, 'winners_go': 59, 'id': 53, 'round': 3},
    {'teams':[], 'ranking': None, 'losers_go': 108, 'winners_go': 59, 'id': 54, 'round': 3},
    {'teams':[], 'ranking': None, 'losers_go': 111, 'winners_go': 60, 'id': 55, 'round': 3},
    {'teams':[], 'ranking': None, 'losers_go': 110, 'winners_go': 60, 'id': 56, 'round': 3},
    {'teams':[], 'ranking': None, 'losers_go': 119, 'winners_go': 61, 'id': 57, 'round': 4},
    {'teams':[], 'ranking': None, 'losers_go': 118, 'winners_go': 61, 'id': 58, 'round': 4},
    {'teams':[], 'ranking': None, 'losers_go': 117, 'winners_go': 62, 'id': 59, 'round': 4},
    {'teams':[], 'ranking': None, 'losers_go': 116, 'winners_go': 62, 'id': 60, 'round': 4},
    {'teams':[], 'ranking': None, 'losers_go': 122, 'winners_go': 63, 'id': 61, 'round': 5},
    {'teams':[], 'ranking': None, 'losers_go': 123, 'winners_go': 63, 'id': 62, 'round': 5},
    {'teams':[], 'ranking': None, 'losers_go': 125, 'winners_go': 126, 'id': 63, 'round': 6},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 80, 'id': 64, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 81, 'id': 65, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 82, 'id': 66, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 83, 'id': 67, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 84, 'id': 68, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 85, 'id': 69, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 86, 'id': 70, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 87, 'id': 71, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 88, 'id': 72, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 89, 'id': 73, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 90, 'id': 74, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 91, 'id': 75, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 92, 'id': 76, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 93, 'id': 77, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 94, 'id': 78, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 95, 'id': 79, 'round': -1},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 100, 'id': 80, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 96, 'id': 81, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 102, 'id': 82, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 97, 'id': 83, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 101, 'id': 84, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 98, 'id': 85, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 103, 'id': 86, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 99, 'id': 87, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 96, 'id': 88, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 100, 'id': 89, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 98, 'id': 90, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 101, 'id': 91, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 97, 'id': 92, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 102, 'id': 93, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 99, 'id': 94, 'round': -2},
    {'teams':[], 'ranking': None, 'losers_go': 0, 'winners_go': 103, 'id': 95, 'round': -2},
    {'teams':[], 'ranking': '24-32th', 'losers_go': 0, 'winners_go': 104, 'id': 96, 'round': -3},
    {'teams':[], 'ranking': '24-32th', 'losers_go': 0, 'winners_go': 105, 'id': 97, 'round': -3},
    {'teams':[], 'ranking': '24-32th', 'losers_go': 0, 'winners_go': 106, 'id': 98, 'round': -3},
    {'teams':[], 'ranking': '24-32th', 'losers_go': 0, 'winners_go': 107, 'id': 99, 'round': -3},
    {'teams':[], 'ranking': '24-32th', 'losers_go': 0, 'winners_go': 108, 'id': 100, 'round': -3},
    {'teams':[], 'ranking': '24-32th', 'losers_go': 0, 'winners_go': 109, 'id': 101, 'round': -3},
    {'teams':[], 'ranking': '24-32th', 'losers_go': 0, 'winners_go': 110, 'id': 102, 'round': -3},
    {'teams':[], 'ranking': '24-32th', 'losers_go': 0, 'winners_go': 111, 'id': 103, 'round': -3},
    {'teams':[], 'ranking': '16-24th', 'losers_go': 0, 'winners_go': 112, 'id': 104, 'round': -4},
    {'teams':[], 'ranking': '16-24th', 'losers_go': 0, 'winners_go': 113, 'id': 105, 'round': -4},
    {'teams':[], 'ranking': '16-24th', 'losers_go': 0, 'winners_go': 112, 'id': 106, 'round': -4},
    {'teams':[], 'ranking': '16-24th', 'losers_go': 0, 'winners_go': 113, 'id': 107, 'round': -4},
    {'teams':[], 'ranking': '16-24th', 'losers_go': 0, 'winners_go': 114, 'id': 108, 'round': -4},
    {'teams':[], 'ranking': '16-24th', 'losers_go': 0, 'winners_go': 115, 'id': 109, 'round': -4},
    {'teams':[], 'ranking': '16-24th', 'losers_go': 0, 'winners_go': 114, 'id': 110, 'round': -4},
    {'teams':[], 'ranking': '16-24th', 'losers_go': 0, 'winners_go': 115, 'id': 111, 'round': -4},
    {'teams':[], 'ranking': '13-16th', 'losers_go': 0, 'winners_go': 116, 'id': 112, 'round': -5},
    {'teams':[], 'ranking': '13-16th', 'losers_go': 0, 'winners_go': 117, 'id': 113, 'round': -5},
    {'teams':[], 'ranking': '13-16th', 'losers_go': 0, 'winners_go': 118, 'id': 114, 'round': -5},
    {'teams':[], 'ranking': '13-16th', 'losers_go': 0, 'winners_go': 119, 'id': 115, 'round': -5},
    {'teams':[], 'ranking': '9-12th', 'losers_go': 0, 'winners_go': 120, 'id': 116, 'round': -6},
    {'teams':[], 'ranking': '9-12th', 'losers_go': 0, 'winners_go': 120, 'id': 117, 'round': -6},
    {'teams':[], 'ranking': '9-12th', 'losers_go': 0, 'winners_go': 121, 'id': 118, 'round': -6},
    {'teams':[], 'ranking': '9-12th', 'losers_go': 0, 'winners_go': 121, 'id': 119, 'round': -6},
    {'teams':[], 'ranking': '7-8th', 'losers_go': 0, 'winners_go': 122, 'id': 120, 'round': -7},
    {'teams':[], 'ranking': '7-8th', 'losers_go': 0, 'winners_go': 123, 'id': 121, 'round': -7},
    {'teams':[], 'ranking': '5-6th', 'losers_go': 0, 'winners_go': 124, 'id': 122, 'round': -8},
    {'teams':[], 'ranking': '5-6th', 'losers_go': 0, 'winners_go': 124, 'id': 123, 'round': -8},
    {'teams':[], 'ranking': '4th', 'losers_go': 0, 'winners_go': 125, 'id': 124, 'round': -9},
    {'teams':[], 'ranking': '3rd', 'losers_go': 0, 'winners_go': 126, 'id': 125, 'round': -10},
    {'teams':[], 'ranking': '2nd', 'losers_go': 0, 'winners_go': 127, 'id': 126, 'round': 7},
    {'teams':[], 'ranking': '1st', 'losers_go': 0, 'winners_go': 0, 'id': 127, 'round': 8} ]


seed = [None,
    11, 19, 3, 27, 21, 13, 29, 5,
    9, 23, 15, 17, 1, 31, 7, 25,
    14, 4, 10, 12, 28, 26, 20, 30,
    32, 18, 24, 22, 6, 8, 2, 16,
    15, 1, 11, 9, 25, 27, 17, 31,
    29, 19, 21, 23, 7, 5, 3, 13,
    16, 2, 12, 10, 26, 28, 18, 32,
    30, 20, 22, 24, 8, 6, 4, 14]


class Bracket():
    def __init__(__, teams ):
        __.teams = teams
        __.match = [None] * 129
        __.team_numbers = len( teams )
        __.byes = 64 - __.team_numbers
        __.bye = __.team_numbers + 1
        if __.byes:
            __.teams[ str(__.team_numbers + 1) ] = 'bye'

        __.match = matches
        for position in teams:
            team_name = teams[ position ]
            position = int( position )
            if position <= 32:
                id = seed[ position ]
                __.match[ id ]['teams'].append( position )
            elif team_name != 'bye':
                id = seed[ position + __.byes ]
                __.match[ id ]['teams'].append( position )

        for row in range(1,33):
            if len( __.match[ row ][ 'teams' ] ) < 2:
                __.match[ row ][ 'teams' ].append( __.bye )

    def report(__, winner_id ):
            ret = []
            match_id = 0
            for row in matches:
                if winner_id in row['teams']:
                    match_id = row['id']
            teams =  __.match[ match_id ]['teams'][:]
            if len(teams) < 2:
                # print 'not yet'
                return

            teams.remove( winner_id )
            loser_id = teams.pop()

            winners_go = __.match[ match_id ]['winners_go']
            if winners_go:
                __.match[winners_go]['teams'].append( winner_id )
            if len(__.match[winners_go]['teams'] ) == 2:
                ret.append(__.match[winners_go])

            losers_go = __.match[ match_id ]['losers_go']
            if losers_go:
                __.match[losers_go]['teams'].append( loser_id )
            if len(__.match[losers_go]['teams'] ) == 2:
                ret.append(__.match[losers_go])
            return ret

