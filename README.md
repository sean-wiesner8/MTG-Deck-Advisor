# Magic The Gathering - Deck Advisor
Python based data pipeline orchestrated with Apache Airfow and containerized with Docker Compose, serving the purpose of simplifying the competitive deck construction process in the popular collectible card game Magic: The Gathering. Tournament deck data scraped from [MTGTop8](https://mtgtop8.com/) and card data scraped from the [Scryfall API](https://scryfall.com/).

## Architecture
Data architecture hosted on AWS and created with Terraform. Services utilized in this pipeline include:
- S3 Buckets: Data lake used to store pre-processed and processed data from both sources
- RDS: There are two relational databases hosted on AWS that are utilized in the data pipeline; an application database which is accessed whenever users retrieve data and a warehouse database for storage and analytics.
- Redshift: Data warehouse which serves as the architecture for data modeling and storage. Soon will be accessed by an analytics page hosted on Metabase for long-term meta trend analysis. 

## Pipeline
Data pipeline orchestrated with Apache Airflow and containerized with Docker Compose. DAG steps:
1. Scrape raw card data from Scryfall API
2. Scrape raw tournament deck data from MTGTop8 with beautifulsoup4
3. Load raw card and deck data from Scryfall API into data lake (AWS S3) with JSON format
4. Validate raw data with Pydantic and transform data into tabular format with Pandas to help facilitate the process of loading data into the relational databases
5. Load prep data into data lake with CSV format
6. Load data into application database (AWS RDS)
7. Load data into data warehouse (AWS Redshift)

