-- normalize table 
delete from display_url;
delete from tweet_norm;
delete from user;
delete from lang;
delete from place;

-- there is no standart sqllite row_number in sqllite - use subquery instead
-- USER
insert into user(name, location)
with tt as
(
	select 
		distinct name
	from
		tweet
)
select 
	name, (select min (location ) from tweet tw where tw.name = tt.name) location
from
	tt;

	-- PLACE
insert into place(country_code)
with tt as
(
	select 
		distinct country_code
	from
		tweet
)
select 
	country_code
from
	tt;
	
	-- LANG
insert into lang(name)
with tt as
(
	select 
		distinct lang
	from
		tweet
)
select 
	lang
from
	tt;	
	
-- insert into tweet_norm
insert into tweet_norm
(
	user_id		
	,tweet_text
	,place_id	
	,lang_id 	
	,created_at	
	,source_id 
	,tweet_id	
)
select	
	u.id 			user_id,
	t.tweet_text	tweet_text,
	p.id			place_id,
	l.id 			lang_id,
	t.created_at	created_at,
	t.source_id		source_id,
	t.tweet_id		tweet_id
from 
	(
		select name, lang, country_code, tweet_text, created_at, max(id) source_id, max(tweet_id) tweet_id 
		from	
			tweet t
		group by 
			name, lang, country_code, tweet_text, created_at
	)t
left join	
	user u on (
		u.name = t.name
	)
left join 
	lang l on (
		l.name = t.lang
	)
left join 
	place p on (
		p.country_code = t.country_code
	)	;
	
insert into display_url (display_url, tweet_norm_id)	
select 
	display_url, tn.id tweet_norm_id
from 
	(
		select distinct display_url, tweet_id
		from	
			tweet t
		where	
			ltrim(rtrim(t.display_url))<>''
	)t
join
	tweet_norm tn on
	(
		tn.tweet_id = t.tweet_id
	);
	
	
--select * from tweet_norm;	