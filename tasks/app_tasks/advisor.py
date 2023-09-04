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


def provide_advice(cursor, deck, arch_id):
    best_lvl_query = f"SELECT lvl FROM Deck WHERE archetype_id = '{arch_id}' ORDER BY lvl DESC LIMIT 1"
    cursor.execute(best_lvl_query)
    best_lvl = cursor.fetchone()[0]
    best_rank_query = f"SELECT rank FROM Deck WHERE archetype_id = '{arch_id}' ORDER BY rank ASC LIMIT 1"
    cursor.execute(best_rank_query)
    best_rank = cursor.fetchone()[0]

    lvl_query = f"SELECT * FROM Deck WHERE archetype_id = '{arch_id}' AND lvl = {best_lvl} ORDER BY rank ASC LIMIT 3"
    rank_query = f"SELECT * FROM Deck WHERE archetype_id = '{arch_id}' AND rank = {best_rank} ORDER BY lvl DESC LIMIT 3"

    cursor.execute(lvl_query)
    lvl_decks_info = cursor.fetchall()
    cursor.execute(rank_query)
    rank_decks_info = cursor.fetchall()

    def get_cards_for_deck(decks):
        named_decks = []
        for d in decks:
            deck_id = d[0]
            get_cards_query = f"SELECT * FROM Cardcount WHERE deck_id = '{deck_id}'"
            cursor.execute(get_cards_query)
            cardcounts = cursor.fetchall()
            named_deck = []
            for card in cardcounts:
                get_cardname_query = f"SELECT name FROM Card WHERE id = '{card[0]}'"
                cursor.execute(get_cardname_query)
                card_name = cursor.fetchone()[0]
                card_count = card[1]
                named_deck.append((card_name, card_count))
            named_decks.append(named_deck)
        return named_decks

    lvl_decks = get_cards_for_deck(lvl_decks_info)
    rank_decks = get_cards_for_deck(rank_decks_info)
    return [lvl_decks, rank_decks]


def main():

    conn = create_conn()
    cursor = conn.cursor()

    print("Hello, welcome to the MTG - Deck Advisor.\n")
    deck_input = input(
        "Input the cards and card counts in your deck. Format: card1; count1 // card2; count2 // etc.: ")
    deck = assemble_deck(deck_input)

    available_archs = get_archetypes(cursor)
    available_archs = "\n".join(available_archs)
    arch_input = input(
        f"What archetype does your deck belong to? Current available archetypes:\n{available_archs}\narchetype: ")
    arch_id = find_archetype(cursor, arch_input)

    advice = provide_advice(cursor, deck, arch_id)
    print(advice)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
