drop table if exists display_url;
drop table if exists tweet_norm;
drop table if exists user;
drop table if exists place;
drop table if exists lang;

create table user
(
	id 			integer primary key,
	name		varchar(20),
	location	varchar(100),
	last_update TIMESTAMP 
	DEFAULT CURRENT_TIMESTAMP
);

create table place
(
	id 				integer primary key,
	country_code	varchar(20),
	last_update 	TIMESTAMP 
	DEFAULT CURRENT_TIMESTAMP
);

create table lang
(
	id 				integer primary key,
	name			varchar(20),
	last_update 	TIMESTAMP 
	DEFAULT CURRENT_TIMESTAMP
);

create table if not exists tweet_norm
( 
	id 			integer primary key AUTOINCREMENT,
	user_id		integer,
	tweet_text	varchar(150), 
	place_id	integer ,
	lang_id 	integer ,
	created_at	DATETIME, 
	source_id   integer,
	tweet_sentiment integer DEFAULT 0,
	foreign key (user_id) references user(id), 
	foreign key (place_id) references place(id), 
	foreign key (source_id) references tweet(id), 
	foreign key (lang_id) references lang(id)
);

create table display_url
(
	id 				integer primary key,
	tweet_norm_id	integer,
	display_url		varchar(255),
	last_update 	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	foreign key (tweet_norm_id) references tweet_norm(id)
	
);

