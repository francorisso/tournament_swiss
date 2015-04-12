#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import psycopg2.extras

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM matches')
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM players')
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    # use cursor_factory to get a dictionary
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT COUNT(players.id) as total FROM players')
    res = cursor.fetchone()
    conn.close()

    return res['total']

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO players(name) VALUES (%(name)s)',
        {'name':name})
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
    A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    # use cursor_factory to get a dictionary
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
        SELECT
            p.id,
            p.name,
            COALESCE(mwon.total,0) as won,
            COALESCE(mwon.total,0)
            + COALESCE(mlost.total,0)
            + COALESCE(mtied.total, 0) as matches
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
        ORDER BY won DESC
        ''')
    results = cursor.fetchall()
    conn.close()

    return results


def reportMatch(tournament_id, player1, player2, result):
    """Records the outcome of a single match between two players.

    Args:
      tournament_id: id of tournament
      player1: id of player 1
      player2: id of player 2
      result: -1 means player1 win, 1 means player2 win, 0 means that was a tie
    """
    conn = connect()
    cursor = conn.cursor()

    # create new match
    cursor.execute('''
        INSERT INTO
            matches(tournament_id)
        VALUES
            (%(tournament_id)s)
        RETURNING id;
        ''',
    { 'tournament_id' : tournament_id })
    match_id = cursor.fetchone()[0]
    if not match_id:
        return False

    # create the results for each player
    if( result==0 ):
        res_player1 = 'tied'
        res_player2 = 'tied'
    elif( result==-1 ):
        res_player1 = 'won'
        res_player2 = 'lost'
    elif( result==-1 ):
        res_player1 = 'lost'
        res_player2 = 'won'
    else:
        return False

    cursor.execute('''
        INSERT INTO
            matches_players(player_id, result)
        VALUES
            (%(player_id)s, %(result)s)
        ''',
    {
        'player_id' : player1,
        'result' : res_player1,
    })

    cursor.execute('''
        INSERT INTO
            matches_players(player_id, result)
        VALUES
            (%(player_id)s, %(result)s)
        ''',
    {
        'player_id' : player2,
        'result' : res_player2,
    })

    conn.commit()
    conn.close()

    return True

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    matches = []
    nextMatch = None
    for row in standings:
        if nextMatch==None:
            nextMatch = [row[0],row[1]]
            continue

        nextMatch.append(row[0])
        nextMatch.append(row[1])
        matches.append(nextMatch)
        nextMatch = None

    return matches