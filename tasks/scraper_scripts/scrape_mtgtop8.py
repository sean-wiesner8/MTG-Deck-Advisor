import requests
from bs4 import BeautifulSoup
import json


class Scraper:

    def __init__(self):
        self.base_url = "https://www.mtgtop8.com/"

    def scrape_all(self, endpoint):
        url = self.base_url + endpoint
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

        except requests.exceptions.RequestException as e:
            print(e)

        else:
            archetypes_raw = soup.body.table.td
            archetypes = archetypes_raw.find_all(
                "div", {"class": "hover_tr", "style": "display:inline-block;width:48%;"})

            json_dict = {'archetypes': []}
            for arch in archetypes:
                arch = arch.find("div", {"style": "display:flex;"}).find(
                    "div", {"style": "width:100%;"})
                name = arch.find("div", {"class": "S14"}).a.string
                link = arch.find("div", {"class": "S14"}).a['href']
                percentage = arch.find_all("div")[1].div.string[:-2]
                dict_archs = json_dict['archetypes']
                dict_archs.append(
                    {'name': name, 'endpoint': link, 'percentage': percentage})
                dict_archs[-1]['decks'] = self.scrape_decks(link)
                print(len(dict_archs[-1]['decks']))

            print(len(json_dict['archetypes']))

            return json_dict

    def scrape_decks(self, endpoint):
        url = self.base_url + endpoint
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

        except requests.exceptions.RequestException as e:
            print(e)

        else:
            decks = soup.body.table.find_all("td", limit=2)[
                1].form.table.find_all("tr", {"class": "hover_tr"})

            ret_decks = []
            for deck in decks:
                deck = deck.find_all("td")
                author = deck[2].string
                event = deck[3].string
                level = len(deck[4].find_all("img"))
                rank = deck[5].string
                date = deck[6].string
                link = deck[1].a['href']
                ret_decks.append({'author': author, 'event': event,
                                 'level': level, 'rank': rank, 'date': date, 'link': link})
                ret_decks[-1]['cards'] = self.scrape_deck(link)

            return ret_decks

    def scrape_deck(self, endpoint):
        url = self.base_url + endpoint
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

        except requests.exceptions.RequestException as e:
            print(e)

        else:
            cards = soup.body.div.div.find("div", {"style": "display:flex;"}).find("div", {
                "style": "width:75%;padding:5px;"}).find("div", {"style": "display:flex;align-content:stretch;"}).find_all("div", {"style": "margin:3px;flex:1;"}, limit=2)

            ret_deck = []
            for column in cards:
                column = column.find_all(
                    "div", {"class": "deck_line hover_tr"})
                for card in column:
                    count = None
                    text = card.text
                    if text[1] != " ":
                        count = text[:2]
                    else:
                        count = text[0]
                    name = card.span.string
                    ret_deck.append({'name': name, 'count': count})

            return ret_deck


def main():
    scraper = Scraper()
    data = scraper.scrape_all('format?f=ST')
    with open('mtgtop8_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
