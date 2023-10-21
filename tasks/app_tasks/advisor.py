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


def find_archetype(cursor, arch):
    query = f"SELECT id FROM Archetype WHERE name = '{arch}'"
    cursor.execute(query)
    raw_id = cursor.fetchone()
    return raw_id[0]


def assemble_deck(deck):
    deck_dict = {}
    for card in deck:
        formatted_card = card.split("; ")
        card_name = formatted_card[0]
        card_count = int(formatted_card[1])
        deck_dict[card_name] = card_count

    return deck_dict


def parse_input(input):
    deck_list = []
    line_num = 0
    line = input[line_num]
    while line[0] != '*':
        if line[0] != '#' and line != '\n':
            deck_list.append(line)
        line_num += 1
        line = input[line_num]

    formatted_deck = assemble_deck(deck_list)
    line_num += 1
    archetype = input[line_num][:-1]
    line_num += 1
    limit = input[line_num]

    return (formatted_deck, archetype, limit)


def get_best_decks(arch_id, cursor, limit):
    query = f"SELECT id FROM deck WHERE archetype_id = '{arch_id}' ORDER BY rank LIMIT {limit}"
    cursor.execute(query)
    raw_ids = cursor.fetchall()
    decks = {}
    for raw_id in raw_ids:
        decks[raw_id[0]] = {}

    for id in decks:
        cardcount_query = f"SELECT card_id, count FROM cardcount WHERE deck_id = '{id}'"
        cursor.execute(cardcount_query)
        raw_deck_data = cursor.fetchall()
        for card_id, count in raw_deck_data:
            cardname_query = f"SELECT name FROM card WHERE id = '{card_id}'"
            cursor.execute(cardname_query)
            card_name = cursor.fetchone()[0]
            decks[id][card_name] = int(count)

    return decks


def find_differences(user_deck, online_deck):
    shared_cards = []
    user_only_cards = []
    online_only_cards = []

    for card in user_deck:
        if card not in online_deck:
            user_only_cards.append((card, user_deck[card]))
        elif user_deck[card] <= online_deck[card]:
            shared_cards.append((card, user_deck[card]))
        else:
            diff = user_deck[card] - online_deck[card]
            shared_cards.append((card, online_deck[card]))
            user_only_cards.append((card, diff))

    for card in online_deck:
        if card not in user_deck:
            online_only_cards.append((card, online_deck[card]))
        elif online_deck[card] > user_deck[card]:
            diff = online_deck[card] - user_deck[card]
            online_only_cards.append((card, diff))

    return (shared_cards, user_only_cards, online_only_cards)


def get_deck_info(deck_id, cursor):
    deck_info_query = f"SELECT author, event_name, rank, date_used FROM deck WHERE id = '{deck_id}'"
    cursor.execute(deck_info_query)
    deck_info = cursor.fetchone()
    deck_info_dict = {
        "author": deck_info[0], "event": deck_info[1], "rank": deck_info[2], "date": deck_info[3]}

    return deck_info_dict


def main():
    conn = create_conn()
    cursor = conn.cursor()

    with open('app_tasks/input.txt') as f:
        input_data = f.readlines()

    formatted_deck, archetype, limit = parse_input(input_data)
    arch_id = find_archetype(cursor, archetype)

    best_decks = get_best_decks(arch_id, cursor, limit)

    with open('app_tasks/output.txt', 'w') as f:
        for i, deck_id in enumerate(best_decks):
            deck_info = get_deck_info(deck_id, cursor)
            author = deck_info["author"]
            event = deck_info["event"]
            rank = deck_info["rank"]
            date = deck_info["date"]
            f.write(f"Deck {i+1}:\n")
            f.write(f"Author: {author}\n")
            f.write(f"Event: {event}\n")
            f.write(f"Rank: {rank}\n")
            f.write(f"Date: {date}\n\n")

            shared, user_only, online_only = find_differences(
                formatted_deck, best_decks[deck_id])

            f.write("Cards contained in both decks:\n")
            for card in shared:
                name = card[0]
                count = card[1]
                f.write(f"{name}, {count}\n")
            f.write("\n")

            f.write("Cards contained in your deck only:\n")
            for card in user_only:
                name = card[0]
                count = card[1]
                f.write(f"{name}, {count}\n")
            f.write("\n")

            f.write(f"Cards contained in {author}'s deck only:\n")
            for card in online_only:
                name = card[0]
                count = card[1]
                f.write(f"{name}, {count}\n")
            f.write("\n***\n\n")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
