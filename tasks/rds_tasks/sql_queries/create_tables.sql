CREATE TABLE IF NOT EXISTS Card(
  id int NOT NULL PRIMARY KEY,
  mtg_id varchar(255),
  name varchar(100),
  released_at varchar(10),
  uri varchar(255),
  scryfall_uri varchar(255),
  mana_cost varchar(25),
  type_line varchar(50),
  oracle_text varchar(500)
)

-- CREATE TABLE IF NOT EXISTS Color(
--   id int NOT NULL PRIMARY KEY,
--   mtg_id varchar(1)
-- )

-- CREATE TABLE IF NOT EXISTS CardColorJoin(
--   card_id int NOT NULL,
--   color_id NOT NULL,
--   FOREIGN KEY (card_id) REFERENCES Card(id),
--   FOREIGN KEY (color_id) REFERENCES Color(id),
--   UNIQUE (card_id, color_id)
-- )

-- CREATE TABLE IF NOT EXISTS Keywords(

-- )