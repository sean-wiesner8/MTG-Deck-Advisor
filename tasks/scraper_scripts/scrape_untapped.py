import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
import pandas as pd
import pyperclip
import time
import sys


class Scraper:
    def scrape_all_decks(address):

        print("selenium version: ")
        print(selenium.__version__)

        path_to_extension = '/opt/airflow/tasks/scraper_scripts/extras/extension_5_8_0_0.crx'
        sys.path.insert(
            0, '/opt/airflow/tasks/chromedriver_linux64/chromedriver')

        options = webdriver.ChromeOptions()
        options.add_extension(path_to_extension)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        driver.maximize_window()
        driver.get(address)
        original_window = driver.current_window_handle
        time.sleep(30)
        driver.switch_to.window(original_window)

        # element = driver.find_element(
        #     By.CSS_SELECTOR, 'button.sc-bdfBQB.sc-dlfnuX.bwRvLb.VlJBq.button.bt-inactive')
        # element.click()

        all_decks = []
        checked_elems = set()
        height = driver.execute_script("return document.body.scrollHeight")
        prev_height = None
        printed = 0
        failed = 0
        deck_num = 0
        while height != prev_height:
            elements = driver.find_elements(
                By.CSS_SELECTOR, 'button.sc-bdfBQB.hZABNZ.button.btn-copy-deck')
            WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, 'button.sc-bdfBQB.hZABNZ.button.btn-copy-deck')))

            prev_height = height
            for elem in elements:
                if elem not in checked_elems:
                    try:
                        deck_num += 1
                        checked_elems.add(elem)
                        deck = {"card_name": [], "count": [],
                                "deck_num": deck_num}

                        elem.click()
                        raw_data = pyperclip.paste()

                        data = raw_data.split('\n')
                        for card_info in data[1:]:
                            card_info = card_info.split(maxsplit=1)
                            count = card_info[0]
                            card_name = card_info[1]
                            deck["card_name"].append(card_name)
                            deck["count"].append(count)

                        deck_df = pd.DataFrame(deck)
                        print(deck_df)
                        printed += 1
                        print("count: " + str(printed))
                        all_decks.append(deck_df)
                    except (StaleElementReferenceException, WebDriverException, IndexError):
                        print("stale element: " + str(elem))
                        failed += 1
                        print("stale count: " + str(failed))

            SCROLL_PAUSE_TIME_1 = 10
            SCROLL_PAUSE_TIME_2 = 5
            SCROLL_AMOUNT = 500
            time.sleep(SCROLL_PAUSE_TIME_1)
            driver.execute_script(
                f"window.scrollBy(0, {SCROLL_AMOUNT});")
            height = driver.execute_script(
                "return document.body.scrollHeight")
            time.sleep(SCROLL_PAUSE_TIME_2)

        driver.quit()
        return all_decks


def scrape_untapped():
    address = 'https://mtga.untapped.gg/meta/decks?min-matches=100&rank=BRONZE_TO_PLATINUM'
    decks = Scraper.scrape_all_decks(address)
    pd.concat(decks).to_csv('example_deck_info.csv')


if __name__ == "__main__":
    scrape_untapped()
