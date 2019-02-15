import datetime
import os
import re
import sys
from dataclasses import dataclass
from typing import List

from dateutil.parser import parse

import cache


@dataclass
class Day:
    date: datetime.date
    blurb: str
    dish_of_the_day: str
    eat_with: str
    top_with: str
    the_other_stuff: str

    def to_dict(self):
        return {
            'blurb': self.blurb,
            'dish_of_the_day': self.dish_of_the_day,
            'eat_with': self.eat_with,
            'top_with': self.top_with,
            'the_other_stuff': self.the_other_stuff,
        }


def list_and_prettify(text: str) -> List[str]:
    t = re.sub(r'\n+', r'\n', text).strip()
    return re.split(r'\n', t)


def parse_text(text_filename):
    with open(text_filename, 'r') as f:
        pages = f.read().split('\f')

    splitters = [
        'Dish of the day',
        'The other stuff',
        'Eat with:',
        'Top with:',
        'Give us',
        'Kom med'
    ]

    cake = None
    days = []

    for index, page in enumerate(pages[1:6]):
        blurb, dish, eat, top, other = map(list_and_prettify,
                                           re.split('|'.join(splitters), page)[
                                           0:5])
        # If Thursday
        if index == 3:
            cake = other[-1]
            other = other[:-1]

        date = parse(blurb[0]).date()

        days.append(Day(
            date=date,
            blurb=blurb,
            dish_of_the_day=dish,
            eat_with=eat,
            top_with=top,
            the_other_stuff=other
        ))

    return days, cake


def main():
    if len(sys.argv) == 1:
        sys.exit("Filename expected")
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        sys.exit("File not found")

    days, cake = parse_text(filename)
    cache.write(days, cake)


if __name__ == '__main__':
    main()
