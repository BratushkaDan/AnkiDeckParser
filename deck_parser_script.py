import os
import sys


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    create_deck_directory()
    file_name = sys.argv[1]
    write_to_file(process_cards_from_file(file_name))


def create_deck_directory():
    try:
        os.mkdir(os.getcwd() + "/decks")
    except FileExistsError:
        pass


def process_cards_from_file(file_name):
    try:
        f = open(f"{file_name}", "r", encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        raise Exception(f"Файл с именем '{file_name}' не найден.")

    cards = []
    blank_lines = 0
    card = {'front': '', 'back': ''}
    current = 'front'

    for line in f:
        line = line.strip()
        if line.strip() == '':
            blank_lines += 1
            if blank_lines == 1:
                current = 'back'
        else:
            blank_lines = 0
        if blank_lines == 0:
            card[current] += line + '<br>'
        if blank_lines == 2:
            blank_lines = 0
            current = 'front'
            cards.append(card)
            card = {'front': '', 'back': ''}

    if not card == cards[-1]:
        cards.append(card)

    return cards


def write_to_file(cards):
    f = open("decks/AnkiDeck.tsv", "w", encoding="utf-8")
    for card in cards:
        f.write(card['front'] + '\t' + card['back'] + '\n')
    f.close()

main()
