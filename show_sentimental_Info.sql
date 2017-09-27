-- 5. Написать 1 SQL скрипт, который выводит наиболее и наименее счастливую страну, локацию и пользователя
-- wtih analytical functions like row_number() script would be better (on MSSQL or ORACLE)
with tt as 
(
	select	
		u.name 			user,
		u.location		location,
		p.country_code 	country,
		tweet_sentiment
	from 
		tweet_norm t
	left join	
		user u on (
			u.id = t.user_id
		)
	left join 
		lang l on (
			l.id = t.lang_id
		)
	left join 
		place p on (
			p.id = t.place_id
		)	
), tt_user as
(
	select user, sum(tweet_sentiment) tweet_sentiment
	from	
		tt
	where 
		user is not null	and user <> ''
	group by
		user
)
, tt_country as
(
	select country, sum(tweet_sentiment) tweet_sentiment
	from	
		tt
	where 
		country is not null	and country <> ''
	group by
		country
), tt_location as
(
	select location , sum(tweet_sentiment) tweet_sentiment
	from	
		tt
	where 
		location is not null	and location <> ''
	group by
		location
)
select 
	(
		select user 
		from
			tt_user	
		order by 
			tweet_sentiment asc
		limit 1 	
	) user_min_sentiment,
	(
		select user 
		from
			tt_user	
		order by 
			tweet_sentiment desc
		limit 1 	
	) user_max_sentiment,
	(
		select country 
		from
			tt_country
		order by 
			tweet_sentiment asc
		limit 1 	
	) country_min_sentiment,
	(
		select country 
		from
			tt_country	
		order by 
			tweet_sentiment desc
		limit 1 	
	) country_max_sentiment	,
	(
		select location
		from
			tt_location
		order by 
			tweet_sentiment asc
		limit 1 	
	) location_min_sentiment,
	(
		select location 
		from
			tt_location	
		order by 
			tweet_sentiment desc
		limit 1 	
	) location_max_sentiment	