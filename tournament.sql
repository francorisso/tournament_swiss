-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TYPE IF EXISTS matchresult;
CREATE TYPE matchresult AS ENUM ('won', 'lost', 'tied');

drop table if exists players cascade;
create table players(
	id serial primary key,
	name text not null
);

drop table if exists tournaments cascade;
create table tournaments(
	id serial primary key,
	name text not null
);

drop table if exists matches cascade;
create table matches(
	id serial primary key,
	tournament_id integer references tournaments(id)
);

drop table if exists matches_players cascade;
create table matches_players(
	match_id integer references matches(id),
	player_id integer references players(id),
	result matchresult
);
CREATE INDEX matches_players_result ON matches_players(result);

-- views created to make queries easier
drop view if exists matches_won;
create view matches_won as
	select player_id, COUNT(*) as total
	from matches_players
	where result = 'won'
	group by player_id;

drop view if exists matches_lost;
create view matches_lost as
	select player_id, COUNT(*) as total
	from matches_players
	where result = 'lost'
	group by player_id;

drop view if exists matches_tied;
create view matches_tied as
	select player_id, COUNT(*) as total
	from matches_players
	where result = 'tied'
	group by player_id;