BEGIN TRANSACTION;


--check for cards that don't exist in temp
DELETE FROM CardColorJoin WHERE card_id IN (
SELECT t1.card_id
FROM CardColorJoin t1
    LEFT JOIN CardColorJoin_temp t2 ON t1.card_id = t2.card_id AND t1.color_id = t2.color_id
WHERE t2.card_id IS NULL
);

DELETE FROM CardKeywordJoin WHERE card_id IN (
SELECT t1.card_id
FROM CardKeywordJoin t1
    LEFT JOIN CardKeywordJoin_temp t2 ON t1.card_id = t2.card_id AND t1.keyword_id = t2.keyword_id
WHERE t2.card_id IS NULL
);

DELETE FROM CardCount WHERE card_id IN (
SELECT t1.card_id
FROM CardCount t1
    LEFT JOIN Card_temp t2 ON t1.card_id = t2.id
WHERE t2.id IS NULL
);

DELETE FROM Deck WHERE id IN (
  SELECT t1.id
  FROM Deck t1
      LEFT JOIN CardCount t2 ON t1.id = t2.deck_id
WHERE t2.id IS NULL
);

TRUNCATE Prices;

DELETE FROM Card WHERE id IN (
SELECT t1.id
FROM Card t1
    LEFT JOIN Card_temp t2 ON t1.name = t2.name
WHERE t2.id IS NULL
);

--load new cards from temp that aren't already in main
INSERT INTO Card (id, name, released_at, uri, scryfall_uri, mana_cost, type_line, oracle_text, set_id, set_name, set_uri, rarity, flavor_text, artist, power, toughness)
SELECT t1.id, t1.name, t1.released_at, t1.uri, t1.scryfall_uri, t1.mana_cost, t1.type_line, t1.oracle_text, t1.set_id, t1.set_name, t1.set_uri, t1.rarity, t1.flavor_text, t1.artist, t1.power, t1.toughness FROM Card_temp t1
      LEFT JOIN Card t2 ON t1.name = t2.name
WHERE t2.id IS NULL;

INSERT INTO CardColorJoin (card_id, color_id)
SELECT t1.card_id, t1.color_id FROM CardColorJoin_temp t1
      LEFT JOIN CardColorJoin t2 ON t1.card_id = t2.card_id AND t1.color_id = t2.color_id
WHERE t2.card_id IS NULL;

INSERT INTO Keyword (id, name)
SELECT t1.id, t1.name FROM Keyword_temp t1
      LEFT JOIN Keyword t2 ON t1.name = t2.name
WHERE t2.id IS NULL;

INSERT INTO CardKeywordJoin (card_id, keyword_id)
SELECT t1.card_id, t1.keyword_id FROM CardKeywordJoin_temp t1
      LEFT JOIN CardKeywordJoin t2 ON t1.card_id = t2.card_id AND t1.keyword_id = t2.keyword_id
WHERE t2.card_id IS NULL;

INSERT INTO Prices
SELECT * FROM Prices_temp;

INSERT INTO Archetype (id, name, endpoint, percentage)
SELECT t1.id, t1.name, t1.endpoint, t1.percentage FROM Archetype_temp t1
      LEFT JOIN Archetype t2 ON t1.name = t2.name
WHERE t2.id IS NULL;

INSERT INTO Deck (id, author, event_name, lvl, rank, date_used, link, archetype_id)
SELECT t1.id, t1.author, t1.event_name, t1.lvl, t1.rank, t1.date_used, t1.link, t1.archetype_id FROM Archetype_temp t1
      LEFT JOIN Archetype t2 ON t1.link = t2.link
WHERE t2.id IS NULL;

INSERT INTO CardCount (id, card_id, count, deck_id)
SELECT t1.id, t1.card_id, t1.count, t1.deck_id FROM CardCount_temp t1
      LEFT JOIN CardCount t2 ON t1.card_id = t2.card_id AND t1.deck_id = t2.deck_id
WHERE t2.card_id IS NULL;




END TRANSACTION;

--drop temp tables

DROP TABLE Card_temp;

DROP TABLE Color_temp;

DROP TABLE CardColorJoin_temp;

DROP TABLE Keyword_temp;

DROP TABLE CardKeywordJoin_temp;

DROP TABLE Prices_temp;

DROP TABLE Archetype_temp;

DROP TABLE Deck_temp;

DROP TABLE CardCount_temp;