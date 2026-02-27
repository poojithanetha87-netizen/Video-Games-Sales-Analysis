-Games
select * from Games_Ds;

--->delete duplicate rows 


Delete from Games_Ds where game_n in (select game_n from (select game_n,title, row_number() over( partition by   title,release_date,team,rating,times_listed,                                         number_of_reviews,genres,summary,reviews,plays,playing,backlogs,
  wishlist order by title) as rn from Games_ds ) as x where x.rn>1) ;

---> Adding two new Colunms to extract month and year from timestamp 
Alter Table Games_Ds
add column R_Month int,
add column R_Year int
;


--->update Month and year columns 
update Games_Ds set
R_Month=extract(month from release_date),
R_Year=extract(year from release_date);

--->wrote a query to find unique genre

SELECT DISTINCT
    TRIM(g) AS genre
FROM Games_Ds
CROSS JOIN LATERAL unnest(
    string_to_array(
        replace(replace(replace(genres, '[', ''), ']', ''), '''', ''),
        ','
    )
) AS g
ORDER BY genre;

--->create Genre table 

Create Table Genre(
Game_n int,
title text,
Adventure Text,
Arcade Text,
Brawler Text,
Card_Board_Game Text,
Fighting Text,
Indie Text,
MOBA Text,
Music Text,
Pinball Text,
Platform Text,
Point_and_Click Text,
Puzzle Text,
Quiz_Trivia Text,
Racing Text,
Real_Time_Strategy Text,
RPG Text,
Shooter text,
Simulator Text,
Sport Text,
Strategy text,
Tactical Text,
Turn_Based_Strategy Text,
Visual_Novel Text);

insert into Genre
select game_n,title,
case when genres like '%Adventure%' then title end as Adventure,
case when genres like '%Arcade%' then title end as Arcade,
case when genres like '%Brawler%' then title end as Brawler,
case when genres like '%Card & Board Game%' then title end as Card_Board_Game,
case when genres like '%Fighting%' then title end as Fighting,
case when genres like '%Indie%' then title end as Indie,
case when genres like '%MOBA%' then title end as MOBA,
case when genres like '%Music%' then title end as Music,
case when genres like '%Pinball%' then title end as Pinball,
case when genres like '%Platform%' then title end as Platform,
case when genres like '%Point-and-Click%' then title end as Point_and_Click,
case when genres like '%Puzzle%' then title end as Puzzle,
case when genres like '%Quiz/Trivia%' then title end as Quiz_Trivia,
case when genres like '%Racing%' then title end as Racing,
case when genres like '%Real Time Strategy%' then title end as Real_Time_Strategy,
case when genres like '%RPG%' then title end as RPG,
case when genres like '%Shooter%' then title end as Shooter,
case when genres like '%Simulator%' then title end as Simulator,
case when genres like '%Sport%' then title end as Sport,
case when genres like '%Strategy%' then title end as Strategy,
case when genres like '%Tactical%' then title end as Tactical,
case when genres like '%Turn Based Strategy%' then title end as Turn_Based_Strategy,
case when genres like '%Visual Novel%' then title end as Visual_Novel
from Games_Ds;

select * from Gener;


--->Data Validation 
select * from Games_Ds where title is null or release_date is null or team is null or rating is null or times_listed is null or number_of_reviews is null or genres is null or  summary is null or reviews is null or plays is null or playing is null  or backlogs is null or r_month is null or r_year is null; 



select * from Games_Ds where release_date is null; 


Sales
select * from VGS;

Create view  Region_Sales as

Select Ranks_,nameg,platform,year_p,genre,publisher,Region,Sales

from 
(
select Ranks_,nameg,platform,year_p,genre,publisher,
'NorthAmerica' as Region, na_sales as Sales from VGS
union all
select Ranks_,nameg,platform,year_p,genre,publisher,
'Europe' , eu_sales from VGS
union all
select Ranks_,nameg,platform,year_p,genre,publisher,
'Japan', jp_sales  from VGS
union all
select Ranks_,nameg,platform,year_p,genre,publisher,
'other' ,other_sales from VGS
) t 
where Sales>0
;

Select Region,Sum(Sales) as Sales from Region_Sales  group by Region order by Sales desc;


Select platform ,Sum(Sales) as Sales from Region_Sales
group by platform order by Sales desc limit 10;

Select Year_P,Count(nameg) as No_of_G_R ,Sum(Sales) as Sales
from Region_Sales group by Year_P order by Year_P;

Select publisher,Sum(Sales) as Sales from Region_Sales 
group by publisher order by Sales Desc limit 10;


Select nameg,Sum(Sales) as Sales from Region_Sales 
group by nameg order by Sales Desc limit 10;


select publisher,No_ofG  ,TotalSales,(TotalSales/no_ofg) as VG from (
Select publisher,Count(distinct nameg) as No_ofG ,Sum(Sales) as TotalSales
from Region_Sales group by publisher ) order by VG Desc;


Select Platform,nameg ,
Row_number() over (partition by platform, order by 
um(Sales) As Sales from Region_Sales
order by platform ,Sales limit Sales 5;

Select * from games_Ds;

create view  Team as
Select g.game_n,g.title,g.release_date,g.rating,g.times_listed,g.number_of_reviews,g.genres,g.plays,g.playing,g.backlogs,g.wishlist,
trim(t) as developer from Games_Ds g
cross join lateral 
unnest(string_to_array(replace(replace(replace(g.team, '[',''),']',''),'''',''),',')) As t;
