-- CREATE DATABASE "Demon Slayer"
--     WITH
--     OWNER = postgres
--     ENCODING = 'UTF8'
--     LC_COLLATE = 'English_South Africa.1252'
--     LC_CTYPE = 'English_South Africa.1252'
--     LOCALE_PROVIDER = 'libc'
--     TABLESPACE = pg_default
--     CONNECTION LIMIT = -1
--     IS_TEMPLATE = False;


-- CREATE TABLE player_data (
--     id SERIAL PRIMARY KEY,
--     player_name VARCHAR(255) NOT NULL,
--     character_name VARCHAR(255),
--     play_time TIMESTAMP NOT NULL,
--     points INT DEFAULT 0
-- );


-- #selects the entire table
SELECT * FROM player_data; 


-- #deletes player data
-- DELETE FROM player_data
-- WHERE id >= 127 AND id <= 144;

-- #selects the most popular character used
-- SELECT character_name, COUNT(*) AS selection_count
-- FROM player_data
-- GROUP BY character_name
-- ORDER BY selection_count DESC
-- LIMIT 3;


-- #selects the highest scoring players
-- SELECT player_name, points
-- FROM player_data
-- ORDER BY points DESC
-- LIMIT 10;



