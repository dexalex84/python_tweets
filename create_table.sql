create table tweet 
( 
	id 			integer primary key AUTOINCREMENT,
	name		varchar(20), 
	tweet_text	varchar(150), 
	country_code	varchar(20), 
	display_url	varchar(255), 
	lang		varchar(100), 
	created_at	DATETIME, 
	location	varchar(100)
);