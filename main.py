from wowsunpack import WoWsUnpack
from fuzzywuzzy import fuzz
import os
import json

GAME_PATH = 'C:\Games\World_of_Warships'
RATIO_THRESHOLD = 75
MAX_KEYS = 2


class Entry:
    '''A struct to store the key, ratio, and value'''

    def __init__(self, key: str, ratio: int, value: str):
        self.key = key
        self.ratio = ratio
        self.value = value

    def __str__(self):
        return f'{self.ratio}|{self.key}|{self.value}'

    def __repr__(self):
        return self.__str__()


def ensure_langs() -> None:
    unpack = WoWsUnpack(GAME_PATH)
    if not os.path.exists('langs'):
        unpack.decodeLanguages()
        print('decoded languages')
        return

    if not os.path.exists('langs\en_lang.json'):
        print('langs folder exists, but en_lang.json is missing')
        unpack.reset()
        unpack.decodeLanguages()
        print('decoded languages')
        return

    print('langs folder is valid')


def read_lang(lang: str) -> dict | None:
    lang_path = os.path.join('langs', lang + '_lang.json')
    if not os.path.exists(lang_path):
        print('lang file not found: ' + lang_path)
        return None

    with open(f'langs\\{lang}_lang.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def find_fuzzy_value(en_lang: dict, value: str) -> list:
    keys = []
    for k, v in en_lang.items():
        match_ratio = fuzz.token_sort_ratio(v, value)
        if match_ratio > RATIO_THRESHOLD:
            keys.append(Entry(k, match_ratio, v))
    keys.sort(key=lambda x: x.ratio, reverse=True)
    return keys[:MAX_KEYS]


if __name__ == '__main__':
    ensure_langs()
    en_lang = read_lang('en')
    # read ja, zh and zh_tw
    ja_lang = read_lang('ja')
    zh_lang = read_lang('zh')
    zh_sg_lang = read_lang('zh_sg')
    zh_tw_lang = read_lang('zh_tw')

    # merge languages with their name
    langs = list(zip([ja_lang, zh_lang, zh_sg_lang, zh_tw_lang], [
                 'Japanese', 'Simplified Chinese', 'SG', 'Traditional Chinese']))

    while True:
        key = input('Enter key: ')
        entries = find_fuzzy_value(en_lang, key)
        if len(entries) == 0:
            print('No matches found')
            continue

        for entry in entries:
            print(entry)
            for lang, lang_name in langs:
                print(f'{lang_name}: {lang[entry.key]}')
            print()
