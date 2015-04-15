#Swiss tournament

This library allows to create a [swiss tournament](http://en.wikipedia.org/wiki/Swiss-system_tournament). 

##Install

If you want/can use [vagrant](https://www.vagrantup.com/ "Vagrant"), you can install this running

`vagrant up`

in the root folder of this library. Then type:

`vagrant ssh`

and once you're logged in, type:

`cd /vagrant`

to enter into the current folder.

##Dependencies
If you don't want to (or can't) use vagrant, then you'll need to install this dependencies:
- postgresql
- python-psycopg2
- python-flask
- python-sqlalchemy
- python-pip
- bleach
- oauth2client
- requests
- httplib2

The file Vagrantfile has the commands for install all this under an ubuntu environment.

##Creating Your Database

Before you can run your code or create your tables, you'll need to use the create database command in psql to create the database. Use the name **tournament** for your database. You will need to have installed psql,

`$ psql`

This will login inside psql console, there you can create the database:

`psql> CREATE DATABASE tournament`

And then you can connect psql to your new database by typing `psql> \c tournament`  and create your tables from the statements in tournament.sql. You can do this in either of two ways:

Paste each statement in to psql.

Use the command `\i tournament.sql` to import the whole file into psql at once.

##Tests

You'll find a test suite in tournament_test.py

##Library

The library is in tournament.py, the functions there are:

`registerPlayer(name)`
Adds a player to the tournament by putting an entry in the database. 

`countPlayers()`
Returns the number of currently registered players.

`deletePlayers()`
Clear out all the player records from the database.

`reportMatch(winner, loser)`
Stores the outcome of a single match between two players in the database.

`deleteMatches()`
Clear out all the match records from the database.

`playerStandings()`
Returns a list of (id, name, wins, matches) for each player, sorted by the number of wins each player has.

`swissPairings()`
Given the existing set of registered players and the matches they have played, generates and returns a list of pairings according to the Swiss system. Each pairing is a tuple (id1, name1, id2, name2), giving the ID and name of the paired players. For instance, if there are eight registered players, this function should return four pairings. 
