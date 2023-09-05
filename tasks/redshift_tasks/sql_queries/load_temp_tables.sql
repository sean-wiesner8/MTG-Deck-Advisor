CREATE TEMP TABLE Card_temp (LIKE Card);

CREATE TEMP TABLE Color_temp (LIKE Color);

CREATE TEMP TABLE CardColorJoin_temp (LIKE CardColorJoin);

CREATE TEMP TABLE Keyword_temp (LIKE Keyword);

CREATE TEMP TABLE CardKeywordJoin_temp (LIKE CardKeywordJoin);

CREATE TEMP TABLE Prices_temp (LIKE Prices);

CREATE TEMP TABLE Archetype_temp (LIKE Archetype);

CREATE TEMP TABLE Deck_temp (LIKE Deck);

CREATE TEMP TABLE CardCount_temp (LIKE CardCount);

COPY Card_temp
FROM
    's3://{bucket_name}/card_data.csv' CREDENTIALS 'aws_access_key_id={aws_access_id};aws_secret_access_key={aws_secret_key}' IGNOREHEADER 1 DELIMITER ',' CSV;

COPY Color_temp
FROM
    's3://{bucket_name}/color_data.csv' CREDENTIALS 'aws_access_key_id={aws_access_id};aws_secret_access_key={aws_secret_key}' IGNOREHEADER 1 DELIMITER ',' CSV;

COPY CardColorJoin_temp
FROM
    's3://{bucket_name}/card_color_data.csv' CREDENTIALS 'aws_access_key_id={aws_access_id};aws_secret_access_key={aws_secret_key}' IGNOREHEADER 1 DELIMITER ',' CSV;

COPY Keyword_temp
FROM
    's3://{bucket_name}/keyword_data.csv' CREDENTIALS 'aws_access_key_id={aws_access_id};aws_secret_access_key={aws_secret_key}' IGNOREHEADER 1 DELIMITER ',' CSV;

COPY CardKeywordJoin_temp
FROM
    's3://{bucket_name}/card_keyword_data.csv' CREDENTIALS 'aws_access_key_id={aws_access_id};aws_secret_access_key={aws_secret_key}' IGNOREHEADER 1 DELIMITER ',' CSV;

COPY Prices_temp
FROM
    's3://{bucket_name}/price_data.csv' CREDENTIALS 'aws_access_key_id={aws_access_id};aws_secret_access_key={aws_secret_key}' IGNOREHEADER 1 DELIMITER ',' CSV;

COPY Archetype_temp
FROM
    's3://{bucket_name}/arch_data.csv' CREDENTIALS 'aws_access_key_id={aws_access_id};aws_secret_access_key={aws_secret_key}' IGNOREHEADER 1 DELIMITER ',' CSV;

COPY Deck_temp
FROM
    's3://{bucket_name}/deck_data.csv' CREDENTIALS 'aws_access_key_id={aws_access_id};aws_secret_access_key={aws_secret_key}' IGNOREHEADER 1 DELIMITER ',' CSV;

COPY CardCount_temp
FROM
    's3://{bucket_name}/cardcount_data.csv' CREDENTIALS 'aws_access_key_id={aws_access_id};aws_secret_access_key={aws_secret_key}' IGNOREHEADER 1 DELIMITER ',' CSV;





