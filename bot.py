import argparse
import configparser
import os

import requests

base_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(base_path, "config.ini"))

rocket_config = config["ROCKET"]
HOOK_URL = rocket_config["URL"]
ICON_URL = rocket_config["ICON"]
CHANNEL = rocket_config["CHANNEL"]
BOT_NAME = rocket_config["BOT_NAME"]


def post(text: str):
    """
    Post the menu to the configured destination
    :param text: A prettified menu
    """
    r = requests.post(
        HOOK_URL,
        json={"text": text, "channel": CHANNEL, "from": BOT_NAME, "icon_url": ICON_URL},
    )
    r.raise_for_status()


def talk():
    """ Gives you a simple prompt to write messages as the bot """
    try:
        while True:
            text = input()
            post(text)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    talk()
