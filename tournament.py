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
      A list of dictionaries with the fields:
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        won: the number of matches the player has won
        lost: the number of matches the player has lost
        tied: the number of matches the player has tied
        matches: the number of matches the player has played
        score: this score is won*3 + tied.
    """
    conn = connect()
    # use cursor_factory to get a dictionary
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
        SELECT
            p.id, p.name,
            mwon.total as won,
            mlost.total as lost,
            mtied.total as tied,
            ( won + lost + tied) as matches,
            ( won*3 + lost) as score,
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
        ORDER BY score DESC
        ''')
    results = conn.fetchall()
    conn.close()

    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """


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


