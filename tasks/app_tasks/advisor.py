import psycopg2
import os
from dotenv import dotenv_values

curr_dir = os.getcwd()
config = dotenv_values(f"{curr_dir}/configuration.env")


def create_conn():
    try:
        conn = psycopg2.connect(
            host=config["rds_instance_endpoint"].split(":")[0],
            port=config["rds_port"],
            user=config["rds_username"],
            password=config["rds_password"],
            dbname=config["rds_database_name"],
        )

        return conn
    except Exception as exception:
        print(exception)


def get_archetypes(cursor):
    query = "SELECT name FROM Archetype"
    cursor.execute(query)
    raw_archs = cursor.fetchall()
    archs = [arch[0] for arch in raw_archs]
    return archs


def find_archetype(cursor, arch):
    query = f"SELECT id FROM Archetype WHERE name = '{arch}'"
    cursor.execute(query)
    raw_id = cursor.fetchone()
    return raw_id[0]


def assemble_deck(deck):

    formatted_deck = deck.split(" // ")
    deck_dict = {}
    for card in formatted_deck:
        formatted_card = card.split("; ")
        card_name = formatted_card[0]
        card_count = int(formatted_card[1])
        deck_dict[card_name] = card_count

    return deck_dict


def find_cards(cursor, card_list):
    query_list = [
        f"SELECT * FROM Card WHERE name = '{card_list[i]}';" for i in range(len(card_list))]
    cards_info = set()
    for query in query_list:
        cursor.execute(query)
        cards_info.add(cursor.fetchone())

    return cards_info


def provide_advice(cursor, deck, cards_info, arch_id):
    best_lvl_query = f"SELECT lvl FROM Deck WHERE archetype_id = '{arch_id}' ORDER BY lvl DESC LIMIT 1"
    cursor.execute(best_lvl_query)
    best_lvl = cursor.fetchone()[0]
    best_rank_query = f"SELECT rank FROM Deck WHERE archetype_id = '{arch_id}' ORDER BY rank ASC LIMIT 1"
    cursor.execute(best_rank_query)
    best_rank = cursor.fetchone()[0]

    lvl_query = f"SELECT * FROM Deck WHERE archetype_id = '{arch_id}' AND lvl = {best_lvl} ORDER BY rank ASC LIMIT 3"
    rank_query = f"SELECT * FROM Deck WHERE archetype_id = '{arch_id}' AND rank = {best_rank} ORDER BY lvl DESC LIMIT 3"

    cursor.execute(lvl_query)
    lvl_decks = cursor.fetchall()
    cursor.execute(rank_query)
    rank_decks = cursor.fetchall()

    return [lvl_decks, rank_decks]


def main():

    conn = create_conn()
    cursor = conn.cursor()

    print("Hello, welcome to the MTG - Deck Advisor.\n")
    deck_input = input(
        "Input the cards and card counts in your deck. Format: card1; count1 // card2; count2 // etc.: ")
    deck = assemble_deck(deck_input)

    card_list = [card for card in deck]

    cards_info = find_cards(cursor, card_list)

    available_archs = get_archetypes(cursor)
    available_archs = "\n".join(available_archs)
    arch_input = input(
        f"What archetype does your deck belong to? Current available archetypes:\n{available_archs}\narchetype: ")
    arch_id = find_archetype(cursor, arch_input)

    advice = provide_advice(cursor, deck, cards_info, arch_id)
    print(advice)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
