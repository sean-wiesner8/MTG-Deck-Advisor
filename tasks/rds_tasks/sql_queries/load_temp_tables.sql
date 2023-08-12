CREATE EXTENSION IF NOT EXISTS aws_s3 CASCADE;

CREATE TEMP TABLE Cardtemp (LIKE Card);

CREATE TEMP TABLE Colortemp (LIKE Color);

CREATE TEMP TABLE CardColorJointemp (LIKE CardColorJoin);

CREATE TEMP TABLE Keywordtemp (LIKE Keyword);

CREATE TEMP TABLE CardKeywordJointemp (LIKE CardKeywordJoin);

CREATE TEMP TABLE Pricestemp (LIKE Prices);

CREATE TEMP TABLE Archetypetemp (LIKE Archetype);

CREATE TEMP TABLE Decktemp (LIKE Deck);

CREATE TEMP TABLE CardCounttemp (LIKE CardCount);

