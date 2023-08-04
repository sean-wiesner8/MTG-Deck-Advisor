import requests
import json
import os


class Scraper:

    def get_standard_cards():

        try:
            response = requests.get(
                'http://api.scryfall.com/cards/search?q=legal:standard', timeout=10)
            response.raise_for_status()
            response = response.content.decode('utf8')
            data = json.loads(response)
            return data

        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)


def scrape_mtg():
    cards = Scraper.get_standard_cards()
    curr_path = os.getcwd()
    new_path = f'{curr_path}/tmp'
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    os.chdir(new_path)
    with open('standard_cards.json', 'w', encoding='utf-8') as f:
        json.dump(cards, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    scrape_mtg()
