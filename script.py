import os
import sys
import re


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


def replace_markdown(card):
    for field in ['front', 'back']:
        bold = set(re.findall(r"\*[^*]*\*", card[field], re.MULTILINE))
        for match in bold:
            card[field] = card[field].replace(match, f'<b>{match[1:-1]}</b>')

        underline = set(re.findall(r"_{2}[^_]*_{2}", card[field], re.MULTILINE))
        for match in underline:
            card[field] = card[field].replace(match, f'<u>{match[2:-2]}</u>')

        italic = set(re.findall(r"_[^_]*_", card[field], re.MULTILINE))
        for match in italic:
            card[field] = card[field].replace(match, f'<i>{match[1:-1]}</i>')

    return card


def replace_cloze_deletions(card):
    deletions = re.findall(r"\d+\({2}(?:(?!\)\))(?!\(\().)+\){2}", card['front'], re.MULTILINE)
    for cloze in deletions:
        m = re.match(r"(\d+\({2})((?:(?!\)\))(?!\(\().)+)(\){2})", cloze, re.MULTILINE)
        card['front'] = card['front'].replace(cloze, '{{c' + m[1][:-2] + '::' + m[2].strip() + '}}')
    return card


def post_process_cards(cards):
    for n, card in enumerate(cards):
        cards[n] = replace_cloze_deletions(replace_markdown(card))
    return cards


def process_cards_from_file(file_name):
    try:
        f = open(f"{file_name}", "r", encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        raise Exception(f"Файл с именем '{file_name}' не найден.")

    cards = []
    blank_lines = 0
    card = {'front': '', 'back': '', 'tags': ''}
    current = 'front'

    for line in f:
        line = line.strip().replace("  ", " ")
        if line == '':
            blank_lines += 1
            if blank_lines == 1:
                current = 'back'
        else:
            blank_lines = 0

        if blank_lines == 0:
            if line.count('---') >= 1:
                card[current] += '<br>'
            elif line.count('==') >= 1:
                tags = re.findall(r'[^=]*$', line)[0]
                card['tags'] = ' '.join(tags.split(','))
            else:
                card[current] += line + '<br>'
        elif blank_lines == 2:
            blank_lines = 0
            current = 'front'
            cards.append(card)
            card = {'front': '', 'back': '', 'tags': ''}

    if not card == cards[-1]:
        cards.append(card)
    return post_process_cards(cards)


def write_to_file(cards):
    f = open("decks/AnkiDeck.tsv", "w", encoding="utf-8")
    for card in cards:
        f.write(card['front'] + '\t' + card['back'] + '\t' + card['tags'] + '\n')
    f.close()


main()
