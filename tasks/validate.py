import json
import pandas as pd
from pydantic import ValidationError
from pydantic_models import MTGData, MTGTop8Data, MTGTop8DataDeck


def parse_data_mtg():

    with open('tmp/standard_cards.json') as f:
        mtg_data = json.load(f)["all_cards"]
    mtg_data = pd.concat([pd.DataFrame(page["data"]) for page in mtg_data])

    remove_list = ['object', 'oracle_id', 'multiverse_ids', 'mtgo_id', 'arena_id', 'tcgplayer_id', 'cardmarket_id', 'lang', 'layout', 'highres_image', 'image_status', 'image_uris', 'finishes', 'set_search_uri',
                   'scryfall_set_uri', 'rulings_uri', 'prints_search_uri', 'collector_number', 'digital', 'full_art', 'textless', 'booster', 'story_spotlight', 'edhrec_rank', 'related_uris', 'purchase_uris', 'card_faces', 'loyalty', 'watermark', 'all_parts', 'frame_effects', 'security_stamp', 'cmc', 'legalities', 'games', 'reserved', 'foil', 'nonfoil', 'oversized', 'promo', 'reprint', 'variation', 'set_type', 'card_back_id', 'artist_ids', 'illustration_id', 'border_color', 'frame', 'penny_rank', 'preview', 'color_indicator', 'produced_mana']
    mtg_data = mtg_data.drop(remove_list, axis=1)

    return mtg_data.dropna().to_dict('records')


def parse_data_mtgtop8():
    with open('tmp/mtgtop8_data.json') as f:
        mtg_top8data = json.load(f)["archetypes"]

    return mtg_top8data


def validate_mtg(data):
    try:
        [MTGData(**card) for card in data]
    except ValidationError as e:
        print(e.errors())


def validate_mtgtop8(data):
    try:
        for arch in data:
            MTGTop8Data(**arch)
            [MTGTop8DataDeck(**deck) for deck in arch['decks']]
    except ValidationError as e:
        print(e.errors())


def main():
    data = parse_data_mtg()
    validate_mtg(data)
    data = parse_data_mtgtop8()
    validate_mtgtop8(data)


if __name__ == "__main__":
    main()
