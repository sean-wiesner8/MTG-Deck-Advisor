CREATE EXTENSION IF NOT EXISTS aws_s3 CASCADE;

CREATE TABLE Card_temp (LIKE Card);

CREATE TABLE Color_temp (LIKE Color);

CREATE TABLE CardColorJoin_temp (LIKE CardColorJoin);

CREATE TABLE Keyword_temp (LIKE Keyword);

CREATE TABLE CardKeywordJoin_temp (LIKE CardKeywordJoin);

CREATE TABLE Prices_temp (LIKE Prices);

CREATE TABLE Archetype_temp (LIKE Archetype);

CREATE TABLE Deck_temp (LIKE Deck);

CREATE TABLE CardCount_temp (LIKE CardCount);

SELECT
    aws_s3.table_import_from_s3(
        'Card_temp',
        '',
        '(format csv, header true)',
        '{s3_bucket}',
        'card_data.csv',
        '{aws_region}',
        '{aws_access_key_id}',
        '{aws_secret_access_key}'
    );

SELECT
    aws_s3.table_import_from_s3(
        'Color_temp',
        '',
        '(format csv, header true)',
        '{s3_bucket}',
        'color_data.csv',
        '{aws_region}',
        '{aws_access_key_id}',
        '{aws_secret_access_key}'
    );

SELECT
    aws_s3.table_import_from_s3(
        'CardColorJoin_temp',
        '',
        '(format csv, header true)',
        '{s3_bucket}',
        'card_color_data.csv',
        '{aws_region}',
        '{aws_access_key_id}',
        '{aws_secret_access_key}'
    );

SELECT
    aws_s3.table_import_from_s3(
        'Keyword_temp',
        '',
        '(format csv, header true)',
        '{s3_bucket}',
        'keyword_data.csv',
        '{aws_region}',
        '{aws_access_key_id}',
        '{aws_secret_access_key}'
    );

SELECT
    aws_s3.table_import_from_s3(
        'CardKeywordJoin_temp',
        '',
        '(format csv, header true)',
        '{s3_bucket}',
        'card_keyword_data.csv',
        '{aws_region}',
        '{aws_access_key_id}',
        '{aws_secret_access_key}'
    );

SELECT
    aws_s3.table_import_from_s3(
        'Prices_temp',
        '',
        '(format csv, header true)',
        '{s3_bucket}',
        'price_data.csv',
        '{aws_region}',
        '{aws_access_key_id}',
        '{aws_secret_access_key}'
    );

SELECT
    aws_s3.table_import_from_s3(
        'Archetype_temp',
        '',
        '(format csv, header true)',
        '{s3_bucket}',
        'arch_data.csv',
        '{aws_region}',
        '{aws_access_key_id}',
        '{aws_secret_access_key}'
    );

SELECT
    aws_s3.table_import_from_s3(
        'Deck_temp',
        '',
        '(format csv, header true)',
        '{s3_bucket}',
        'deck_data.csv',
        '{aws_region}',
        '{aws_access_key_id}',
        '{aws_secret_access_key}'
    );

SELECT
    aws_s3.table_import_from_s3(
        'CardCount_temp',
        '',
        '(format csv, header true)',
        '{s3_bucket}',
        'cardcount_data.csv',
        '{aws_region}',
        '{aws_access_key_id}',
        '{aws_secret_access_key}'
    );



