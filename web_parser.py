import configparser
import os
from typing import List

import requests
import re
import datetime
import html

base_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(base_path, 'config.ini'))

rocket_config = config['ROCKET']

ALLERGEN_MAP = {
    'sulfur-dioxide-sulfites': None,
    'mushrooms': None,
    'celery': None,
    'eggs': None,
    'gluten': ":bread:",
    'mustard': None,
    'sesame-seeds': None,
    'milk-lactose': ":milk:",
    'soy': None,
    'fish': ":fish:",
    'shellfish': None,
    'nuts': ":contains-nuts:",
    'peanuts': None,
}

MENU_URL = config['MENU']['URL']
HOOK_URL = rocket_config['URL']
ICON_URL = rocket_config['ICON']
CHANNEL = rocket_config['CHANNEL']
BOT_NAME = rocket_config['BOT_NAME']


def get_menu():
    date = datetime.date.today()
    urls = generate_urls(date)
    menu_json = fetch_menu(urls)
    menu = extract_menu(menu_json, date)

    return menu


def fetch_menu(urls):
    for url in urls:
        try:
            r = requests.get(url)
            menu_json = r.json()
            if menu_json:
                return menu_json
        except:
            pass
    raise Exception('No menu found')


def extract_menu(menu_json: dict, date: datetime.date) -> str:
    """Extract a pretty, formatted menu ready for posting"""

    # It's a list, for whatever reason
    inner_menu = menu_json[-1]
    acf = inner_menu.get('acf')

    date_string = f"*Menu for {date}*"
    story = prettify(acf.get('story')).strip()
    menu_items = parse_menu_items(acf.get('menu_items'))

    return "\n".join([date_string] + [story] + menu_items)


def parse_menu_items(menu_items: list) -> List[str]:
    def parse_menu_item(menu_item: dict) -> str:
        text = menu_item.get('text').strip()

        allergens = menu_item.get('allergens')
        allergen_emojis = []
        if allergens:
            for allergen in allergens:
                allergen_key = allergen.get('slug')
                emoji = ALLERGEN_MAP.get(allergen_key)
                if emoji:
                    allergen_emojis.append(emoji)

        return f'{text} {" ".join(allergen_emojis)}'.strip()

    handlers = {
        'menu_title': lambda text: f"\n*{text}*",
        'menu_description': lambda text: f"*{text}*",
        'menu_item': parse_menu_item,
    }

    parsed_items = []

    for item in menu_items:
        item_type = item.get('acf_fc_layout')
        item_text = item.get(item_type)
        parsed_item = prettify(handlers[item_type](item_text))
        parsed_items.append(parsed_item)

    return parsed_items


def prettify(item: str) -> str:
    item = re.sub('<.+?>', '', item)
    return html.unescape(item)


def generate_urls(date: datetime.date):
    date_string = date.strftime('%B-%-d-%Y').lower()
    url_tday = (
        f"https://trouble.tools/506/wp-json/wp/v2/multiple-post-type"
        f"?slug={date_string}-thoughtful-t-day&type[]=page&type[]=topic&type[]=story&"
        f"type[]=product&type[]=collection&type[]=event&type[]=menu&"
        f"type[]=person&type[]=recipe"
    )
    url = (
        f"https://trouble.tools/506/wp-json/wp/v2/multiple-post-type"
        f"?slug={date_string}&type[]=page&type[]=topic&type[]=story&"
        f"type[]=product&type[]=collection&type[]=event&type[]=menu&"
        f"type[]=person&type[]=recipe"
    )
    return url_tday, url


def post(text: str):
    r = requests.post(
        HOOK_URL,
        json={'text': text, 'channel': CHANNEL, 'from': BOT_NAME, 'icon_url': ICON_URL},
    )
    r.raise_for_status()


def main():
    menu = get_menu()
    post(menu)


if __name__ == '__main__':
    main()
