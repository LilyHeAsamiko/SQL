-- Find all award_name given movie name
SELECT award_name FROM "awards" WHERE "film_name" == 'The DIVORCE';

-- Find all film_info ON given movie name
SELECT * FROM "movies" WHERE "name" = "A Corner in the City";

-- Find all film_name given award_name
SELECT film_name FROM "awards" WHERE "award_name" = "Best Feature Film";

-- Add a new entry
INSERT INTO "2024_SIFF" ("film_name",
	"director_name"
)
 VALUES ('Starfall','Zhang Dalei');

-- Add a new award
INSERT INTO "awards" ("award_name",
    "actor/actress_name",
    "film_name",
    "director_name" 
)
VALUES ('Best Feature Film', NULL,'The DIVORCE', 'Daniyar Salamat');

-- Add a new movie
INSERT INTO "movies" ("id","name","film_genre","film_duration","film_year","film_historic_coutries","film_scores","film_ratings","film_short_synopsis","film_trailor_url","film_intro_url")
VALUES (416428,"A Corner in the City","Drama",113,1983,"China",NULL,NULL,"",NULL,'https://mubi.com/en/hk/films/a-corner-in-the-city'});

-- Add a new cast_info
INSERT INTO "cast_info" ("id","name","position")
VALUES ('221540','W',"Director");