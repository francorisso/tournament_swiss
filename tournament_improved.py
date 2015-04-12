#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import psycopg2.extras

def playerStandings():
    conn = connect()
    # use cursor_factory to get a dictionary
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
        SELECT
            p.id, p.name,
            mwon.total as won,
            mlost.total as lost,
            mtied.total as tied,
            ( won + lost + tied) as matches
        FROM
            players p
        LEFT JOIN
            matches_won mwon
            ON p.id = mwon.player_id
        LEFT JOIN
            matches_lost mlost
            ON p.id = mlost.player_id
        LEFT JOIN
            matches_tied mtied
            ON p.id = mtied.player_id
        ''')
    results = conn.fetchall()
    conn.close()

    return results