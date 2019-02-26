from typing import List

import requests
import re
import datetime
import html


def get_menu():
    date = datetime.date.today()
    urls = generate_urls(date)
    menu_json = fetch_menu(urls)
    menu = extract_menu(menu_json, date)

    return menu


def fetch_menu(urls):
    for url in urls:
        try:
            print(url)
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
    story = parse_story(acf.get('story'))
    menu_items = parse_menu_items(acf.get('menu_items'))

    return "\n".join([date_string] + [story] + menu_items)


def parse_story(story: str) -> str:
    story = re.sub('<p>|</p>', '', story).strip()
    return story


def parse_menu_items(menu_items: list) -> List[str]:

    allergen_map = {
        'sulfur-dioxide-sulfites': ":wine_glass:",
        'mushrooms': ":mushroom:",
        'celery': ":shrug:",
        'eggs': ":egg:",
        'gluten': ":bread:",
        'mustard': ":shrug:",
        'sesame-seeds': ":shrug:",
        'milk-lactose': ":milk:",
        'soy': ":shrug:",
        'fish': ":fish:",
        'shellfish': ":crab:",
        'nuts': ":shrug:",
        'peanuts': ":peanuts:",
    }

    def parse_menu_item(menu_item: dict) -> str:
        text = menu_item.get('text').strip()

        allergens = menu_item.get('allergens')
        allergen_emojis = []
        if allergens:
            for allergen in allergens:
                allergen_emojis.append(allergen_map[allergen.get('slug')])

        return f'{text} {" ".join(allergen_emojis)}'.strip()

    def prettify_menu_item(menu_item: str) -> str:
        conversion_map = {
            '<em>': '_',
            '</em>': '_',
            '<b>': '*',
            '</b>': '*',
        }
        return html.unescape(menu_item)

    handlers = {
        'menu_title': lambda text: f"\n*{text}*",
        'menu_description': lambda text: f"*{text}*",
        'menu_item': parse_menu_item,
    }

    parsed_items = []

    for item in menu_items:
        item_type = item.get('acf_fc_layout')
        item_text = item.get(item_type)
        parsed_item = prettify_menu_item(handlers[item_type](item_text))
        parsed_items.append(parsed_item)

    return parsed_items


def generate_urls(date: datetime.date):
    date_string = 'may-2-2019'
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


def main():
    menu = get_menu()
    print(menu)


if __name__ == '__main__':
    main()
