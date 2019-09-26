import configparser
import datetime
import os

import requests

base_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(base_path, 'config.ini'))

rocket_config = config['ROCKET']

MENU_URL = config['MENU']['URL']
HOOK_URL = rocket_config['URL']
ICON_URL = rocket_config['ICON']
CHANNEL = rocket_config['CHANNEL']
BOT_NAME = rocket_config['BOT_NAME']


def get_menu() -> dict:
    r = requests.get(MENU_URL)
    r.raise_for_status()
    return r.json()


def get_cake() -> dict:
    r = requests.get(f'{MENU_URL}/cake')
    r.raise_for_status()
    return r.json()


def prettify(text):
    return "\n".join(text)


def format_menu(menu: dict) -> str:
    today = datetime.date.today()

    menu_text = f"""*Menu for {today}*:
{menu['blurb']}

*Dish of the day*
{prettify(menu['dish_of_the_day'])}
*Eat with*
{prettify(menu['eat_with'])}"""

    if menu.get('top_with'):
        menu_text += f"""
*Top with*
{prettify(menu['top_with'])}"""

    menu_text += f"""

*The other stuff*
{prettify(menu['the_other_stuff'])}"""

    return menu_text


def format_cake(cake: dict) -> str:
    cake_text = f"""
    *Cake*
    {cake['cake']}
    """
    return cake_text


def post(text: str):
    r = requests.post(HOOK_URL, json={
        'text': text,
        'channel': CHANNEL,
        'from': BOT_NAME,
        'icon_url': ICON_URL
    })
    r.raise_for_status()


def main():
    menu = get_menu()
    menu_text = format_menu(menu)

    weekday = datetime.date.today().isoweekday()
    # If Thursday
    if weekday == 4:
        cake = get_cake()
        cake_text = format_cake(cake)
        menu_text += cake_text

    post(menu_text)


if __name__ == '__main__':
    main()
