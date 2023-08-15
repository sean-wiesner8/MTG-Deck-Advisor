import requests
import json
import os


class Scraper:

    def get_standard_cards():

        try:
            base_url = 'http://api.scryfall.com/cards/search?q=legal:standard'
            response = requests.get(
                base_url, timeout=10)
            response.raise_for_status()
            response = response.content.decode('utf8')
            data = json.loads(response)
            data_list = [data]
            curr_page = 1
            while data["has_more"]:
                curr_page += 1
                response = requests.get(
                    base_url + f"&page={curr_page}", timeout=10)
                response.raise_for_status()
                response = response.content.decode('utf8')
                data = json.loads(response)
                data_list.append(data)
            return data_list

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
    cards = {"all_cards": cards}
    new_path = f"{os.getcwd()}/tmp"
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    os.chdir(new_path)
    with open('standard_cards.json', 'w', encoding='utf-8') as f:
        json.dump(cards, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    scrape_mtg()
