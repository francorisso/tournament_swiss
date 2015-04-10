-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


create table players(
	id serial primary key,
	name text not null
);

create table tournaments(
	id serial primary key,
	name text not null
);

create table matches(
	id serial primary key,
	tournament_id integer references tournaments(id),
	player1 integer references players(id),
	player2 integer references players(id),
);

create table matches_results(
	match_id integer primary key references matches(id),
	winner integer references players(id)
);

-- view created to make queries about player wins easier
create view players_wins as
	select p.id, p.name, count(mr.match_id) as wins
	from players as p
	left join matches_results as mr
		on p.id = mr.winner
	group by p.id;