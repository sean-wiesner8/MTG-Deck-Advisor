# Magic The Gathering - Deck Advisor
Python based data pipeline orchestrated with Apache Airfow and containerized with Docker Compose, serving the purpose of simplifying the competitive deck construction process in the popular collectible card game Magic: The Gathering. Tournament deck data scraped from [MTGTop8](https://mtgtop8.com/) and card data scraped from the [Scryfall API](https://scryfall.com/).

## Architecture
Data architecture hosted on AWS and created with Terraform. Services utilized in this pipeline include:
- S3 Buckets: Data lake used to store pre-processed and processed data from both sources.
- RDS: Two relational databases hosted on AWS that are utilized in the data pipeline; an application database which is accessed whenever users retrieve data and a warehouse database for storage and analytics.
- Redshift: Data warehouse which serves as the architecture for data modeling and storage. Soon will be accessed by an analytics page hosted on Metabase for long-term meta trend analysis. 

## Pipeline
![Illustration of the data pipeline](/images/pipeline.png)
Data pipeline orchestrated with Apache Airflow and containerized with Docker Compose. 
DAG steps:
1. Scrape raw card data from Scryfall API.
2. Scrape raw tournament deck data from MTGTop8 with beautifulsoup4.
3. Load raw card and deck data from Scryfall API into data lake (AWS S3) with JSON format.
4. Validate raw data with Pydantic and transform data into tabular format with Pandas to help facilitate the process of loading data into the relational databases.
5. Load prep data into data lake with CSV format.
6. Load data into application database (AWS RDS).
7. Load data into data warehouse (AWS Redshift).

## Application
The application allows a user to input their person deck information and receive comparisons between their deck and a number of decks (specified by the user) that have performed well recently in tournaments belonging to the same archetype.  

### Run Application

First, run the commands:
```
pipenv update
pipenv shell
```
These commands will install all required dependencies and activate the virtual environment.

Next, create a valid .txt file in the `tasks/app_tasks` directory. 
Format of .txt file:
- Any line that begins with a '#' character is considered to be a comment and is not considered by the program.
- Empty lines are ignored.
- Card input should be in the format "{card name}; {count}", where each card is separated by a new line.
- A line consisting of a single '*' character signals the end of the deck input. 
- The following line of the input is the name of the archetype that your deck belongs to.
- The final line of the input is an integer representing the number of decks you would like the program to output.
Example of properly formatted `input.txt` file consisting of a deck with 16 total cards (3 unique cards), the "Red Deck Wins" archetype, and a request to receive feedback from 3 high-performing tournament decks:
```
Mountain; 10
Furnace Punisher; 4
Khenra Spellspear // Gitaxian Spellstalker; 2
*
Red Deck Wins
3
```

Once the input file has been created, simple run the commands:
```
cd tasks
python3 app_tasks/advisor.py
```
This will output a .txt file in the `tasks/app_tasks` directory containing the similarities and differences between the input deck and top performing decks belonging to the same archetype, as well as some metadata relating to those decks. 
Here is the `output.txt` file created given the example input provided earlier:
```
Deck 1:
Author: ura_frst
Event: MTGO Challenge 32
Rank: 1
Date: 20/08/23

Cards contained in both decks:
Mountain, 10

Cards contained in your deck only:
Furnace Punisher, 4
Khenra Spellspear // Gitaxian Spellstalker, 2

Cards contained in ura_frst's deck only:
Mishra's Foundry, 4
Mountain, 7
Sokenzan, Crucible of Defiance, 1
Bloodthirsty Adversary, 4
Feldon, Ronom Excavator, 3
Monastery Swiftspear, 4
Phoenix Chick, 4
Squee, Dubious Monarch, 3
Lightning Strike, 4
Nahiri's Warcrafting, 4
Play with Fire, 4
Strangle, 4
Kumano Faces Kakkazan // Etching of Kumano, 4

***

Deck 2:
Author: joaoclaudioms
Event: MTGO Preliminary
Rank: 1
Date: 23/08/23

Cards contained in both decks:
Mountain, 10
Furnace Punisher, 4

Cards contained in your deck only:
Khenra Spellspear // Gitaxian Spellstalker, 2

Cards contained in joaoclaudioms's deck only:
Mishra's Foundry, 4
Mountain, 7
Sokenzan, Crucible of Defiance, 2
Bloodthirsty Adversary, 4
Falkenrath Pit Fighter, 2
Feldon, Ronom Excavator, 3
Monastery Swiftspear, 4
Phoenix Chick, 2
Thundering Raiju, 4
Lightning Strike, 4
Play with Fire, 4
Strangle, 2
Kumano Faces Kakkazan // Etching of Kumano, 4

***

Deck 3:
Author: Nitta Shinya
Event: Summer Thanksgiving Tournaments
Rank: 1
Date: 20/08/23

Cards contained in both decks:
Mountain, 10
Furnace Punisher, 3

Cards contained in your deck only:
Furnace Punisher, 1
Khenra Spellspear // Gitaxian Spellstalker, 2

Cards contained in Nitta Shinya's deck only:
Mishra's Foundry, 4
Mountain, 7
Sokenzan, Crucible of Defiance, 2
Bloodthirsty Adversary, 4
Feldon, Ronom Excavator, 3
Monastery Swiftspear, 4
Riveteers Requisitioner, 4
Lightning Strike, 4
Nahiri's Warcrafting, 3
Play with Fire, 4
Invasion of Regatha // Disciples of the Inferno, 4
Kumano Faces Kakkazan // Etching of Kumano, 4

***

```



## Coming Soon
There are a number of new features that I will be adding to the pipeline soon:
1. dbt models to run analysis on meta in ways that have not been done before (e.g. examining macro meta trends).
2. Metabase integration to visualize meta analysis.
3. Web application to make application more user friendly (e.g. visualization of cards).
4. Add data sources with deck information on non-tournament play to improve analytics.

