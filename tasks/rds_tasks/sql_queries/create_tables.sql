-- MTG Scryfall data tables
CREATE TABLE IF NOT EXISTS Card(
  id int NOT NULL PRIMARY KEY,
  name varchar(100),
  released_at varchar(10),
  uri varchar(255),
  scryfall_uri varchar(255),
  mana_cost varchar(25),
  type_line varchar(255),
  oracle_text varchar(1000),
  set_id varchar(50),
  set_name varchar(75),
  set_uri varchar(255),
  rarity varchar(15),
  flavor_text varchar(1000),
  artist varchar(50),
  power varchar(5), -- TODO: change these into ints!!
  toughness varchar(5)
);

CREATE TABLE IF NOT EXISTS Color(
  id int NOT NULL PRIMARY KEY,
  mtg_id varchar(1)
);

CREATE TABLE IF NOT EXISTS CardColorJoin(
  card_id int NOT NULL,
  color_id int NOT NULL,
  FOREIGN KEY (card_id) REFERENCES Card(id),
  FOREIGN KEY (color_id) REFERENCES Color(id),
  UNIQUE (card_id, color_id)
);

CREATE TABLE IF NOT EXISTS Keyword(
  id int NOT NULL PRIMARY KEY,
  name varchar(50)
);

CREATE TABLE IF NOT EXISTS CardKeywordJoin(
  card_id int NOT NULL,
  keyword_id int NOT NULL,
  FOREIGN KEY (card_id) REFERENCES Card(id),
  FOREIGN KEY (keyword_id) REFERENCES Keyword(id)
);

CREATE TABLE IF NOT EXISTS Prices(
  id int NOT NULL PRIMARY KEY,
  usd varchar(15), --TODO: change these into ints!!
  usd_foil varchar(15),
  usd_etched varchar(15),
  eur varchar(15),
  eur_foil varchar(15),
  tix varchar(15),
  card_id int NOT NULL,
  FOREIGN KEY (card_id) REFERENCES Card(id)
);

-- MTGTop8 data tables
CREATE TABLE IF NOT EXISTS Archetype(
  id int NOT NULL PRIMARY KEY,
  name varchar(100),
  endpoint varchar(255),
  percentage varchar(4)
);

CREATE TABLE IF NOT EXISTS Deck(
  id int NOT NULL PRIMARY KEY,
  author varchar(100),
  event_name varchar(100),
  lvl int,
  rank varchar(5),
  date_used varchar(25),
  link varchar(255),
  archetype_id int NOT NULL,
  FOREIGN KEY (archetype_id) REFERENCES Archetype(id)
);

CREATE TABLE IF NOT EXISTS CardCount(
  id int NOT NULL PRIMARY KEY,
  card_id int NOT NULL,
  FOREIGN KEY (card_id) REFERENCES Card(id),
  count varchar(4),
  deck_id int NOT NULL,
  FOREIGN KEY (deck_id) REFERENCES Deck(id)
);

