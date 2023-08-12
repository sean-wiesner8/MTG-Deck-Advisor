import json
import pandas as pd
from pydantic import ValidationError
from pydantic_models import MTGData, MTGTop8Data, MTGTop8DataDeck
import os
from copy import deepcopy


def parse_data_mtg():

    # os.chdir(curr_dir)
    # os.chdir('/opt/airflow/tasks')
    with open('tmp/standard_cards.json') as f:
        mtg_data_raw = json.load(f)["all_cards"]

    mtg_data = []
    for page in mtg_data_raw:
        cards_data = page["data"]
        for card in cards_data:
            mtg_data.append(card)

    mtg_data = pd.DataFrame(mtg_data)

    remove_list = ['object', 'oracle_id', 'multiverse_ids', 'mtgo_id', 'arena_id', 'tcgplayer_id', 'cardmarket_id', 'lang', 'layout', 'highres_image', 'image_status', 'image_uris', 'finishes', 'set_search_uri',
                   'scryfall_set_uri', 'rulings_uri', 'prints_search_uri', 'collector_number', 'digital', 'full_art', 'textless', 'booster', 'story_spotlight', 'edhrec_rank', 'related_uris', 'purchase_uris', 'card_faces', 'loyalty', 'watermark', 'all_parts', 'frame_effects', 'security_stamp', 'cmc', 'legalities', 'games', 'reserved', 'foil', 'nonfoil', 'oversized', 'promo', 'reprint', 'variation', 'set_type', 'card_back_id', 'artist_ids', 'illustration_id', 'border_color', 'frame', 'penny_rank', 'preview', 'color_indicator', 'produced_mana', 'color_identity', 'id']
    mtg_data = mtg_data.drop(remove_list, axis=1)
    ids = pd.Series(mtg_data.index.to_list())
    mtg_data.insert(0, "id", ids)

    return mtg_data


def parse_data_mtgtop8():

    curr_dir = os.getcwd()
    os.chdir(curr_dir)
    # os.chdir('/opt/airflow/tasks')
    with open('tmp/mtgtop8_data.json') as f:
        mtgtop8_data = json.load(f)["archetypes"]
    mtgtop8_data = pd.DataFrame(mtgtop8_data)
    ids = pd.Series(mtgtop8_data.index.to_list())
    mtgtop8_data.insert(0, "id", ids)

    return mtgtop8_data


def validate_mtg(data):

    data = data.to_dict('records')

    try:
        [MTGData(**card) for card in data]
    except ValidationError as e:
        print(e.errors())


def validate_mtgtop8(data):

    data = data.to_dict('records')

    try:
        for arch in data:
            MTGTop8Data(**arch)
            for deck in arch['decks']:
                MTGTop8DataDeck(**deck)
    except ValidationError as e:
        print(e.errors())


def data_to_table(mtg_data, mtgtop8_data):

    # card data
    card_data = mtg_data.drop(['colors', 'keywords', 'prices'], axis=1)

    # colors data
    colors_data = mtg_data['colors']
    color_set = set()

    def add_colors(colors):
        if type(colors) != float:  # check for NaN values
            [color_set.add(color) for color in colors]

    colors_data.apply(add_colors)
    color_data = pd.DataFrame(list(color_set), columns=['mtg_id'])
    color_ids = pd.Series(color_data.index.to_list())
    color_data.insert(0, "id", color_ids)

    # card color join
    card_color_set = set()

    def add_card_color(data):
        colors = data['colors']
        if type(colors) != float:  # check for NaN values
            for color in colors:
                card_color_set.add(
                    (data['id'], color_data.index[color_data['mtg_id']
                                                  == color].to_list()[0]))

    mtg_data.apply(add_card_color, axis=1)
    card_color_data = pd.DataFrame(
        list(card_color_set), columns=['card_id', 'color_id'])
    card_color_ids = pd.Series(card_color_data.index.to_list())
    card_color_data.insert(0, "id", card_color_ids)

    # keywords data
    keywords_data = mtg_data['keywords']
    keyword_set = set()

    def add_keywords(keywords):
        [keyword_set.add(keyword) for keyword in keywords]
    keywords_data.apply(add_keywords)
    keyword_data = pd.DataFrame(list(keyword_set), columns=['name'])
    keyword_ids = pd.Series(keyword_data.index.to_list())
    keyword_data.insert(0, "id", keyword_ids)

    # card keyword join
    card_keyword_set = set()

    def add_card_keyword(data):
        keywords = data['keywords']
        for keyword in keywords:
            card_keyword_set.add(
                (data['id'], keyword_data.index[keyword_data['name'] == keyword].to_list()[0]))

    mtg_data.apply(add_card_keyword, axis=1)
    card_keyword_data = pd.DataFrame(
        list(card_keyword_set), columns=['card_id', 'keyword_id'])
    card_keyword_ids = pd.Series(card_keyword_data.index.to_list())
    card_keyword_data.insert(0, "id", card_keyword_ids)

    # prices data
    prices_data_lst = []

    def add_prices(card):
        prices = card['prices']
        prices['card_id'] = card['id']
        prices_data_lst.append(prices)

    mtg_data.apply(add_prices, axis=1)
    price_data = pd.DataFrame(prices_data_lst)
    price_data_ids = pd.Series(price_data.index.to_list())
    price_data.insert(0, "id", price_data_ids)

    # archetype data
    arch_data = mtgtop8_data.drop('decks', axis=1)

    # deck data
    deck_data_lst = []

    def add_decks(arch):
        decks = arch['decks']
        for deck in decks:
            del deck['cards']
            deck['archetype_id'] = arch['id']
            deck_data_lst.append(deck)

    mtgtop8_data_cp = pd.DataFrame(deepcopy(mtgtop8_data.to_dict()))
    mtgtop8_data_cp.apply(add_decks, axis=1)
    deck_data = pd.DataFrame(deck_data_lst)
    deck_data_ids = pd.Series(deck_data.index.to_list())
    deck_data.insert(0, "id", deck_data_ids)

    # cardcount data
    cardcount_lst = []

    def add_cardcounts(arch):
        nonlocal deck_data
        decks = arch['decks']
        for deck in decks:
            deck_data_loc = deck_data.loc[deck_data['link']
                                          == deck['link']].iloc[0]["id"]
            for card in deck['cards']:
                card_name = card['name']
                count = card['count']
                card_id = card_data.loc[card_data['name'].str.contains(
                    card_name)]
                # Remove decks that aren't standard due to improper deck imports by mtgtop8.com users
                if len(card_id) > 0:
                    card_id = card_id.iloc[0]["id"]
                    cardcount_lst.append(
                        {"card_id": card_id, "count": count, "deck_id": deck_data_loc})
                else:
                    deck_data = deck_data.drop(deck_data_loc)

    mtgtop8_data_cp = pd.DataFrame(deepcopy(mtgtop8_data.to_dict()))
    mtgtop8_data_cp.apply(add_cardcounts, axis=1)
    cardcount_data = pd.DataFrame(cardcount_lst)
    cardcount_data_ids = pd.Series(cardcount_data.index.to_list())
    cardcount_data.insert(0, "id", cardcount_data_ids)

    return {"card_data": card_data, "color_data": color_data, "card_color_data": card_color_data, "keyword_data": keyword_data, "card_keyword_data": card_keyword_data, "price_data": price_data, "arch_data": arch_data, "deck_data": deck_data, "cardcount_data": cardcount_data}


def main():

    mtg_data = parse_data_mtg()
    mtgtop8_data = parse_data_mtgtop8()

    validate_mtg(mtg_data)
    validate_mtgtop8(mtgtop8_data)

    tabular_data = data_to_table(mtg_data, mtgtop8_data)

    # remove ids for csv formatting
    for key in tabular_data:
        tabular_data[key] = tabular_data[key].drop('id', axis=1)

    os.chdir(f"{os.getcwd()}/tmp")
    for key in tabular_data:
        tabular_data[key].to_csv(key)


if __name__ == "__main__":
    main()
