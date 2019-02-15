import datetime
import json
import os
from typing import List
from parser import Day

CACHE_DIR = os.getenv('CACHE_DIR', 'cache')


def write(days: List[Day], cake: str):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    year, week, _ = days[0].date.isocalendar()

    for day in days:
        filename = os.path.join(CACHE_DIR, f'{day.date.isoformat()}.json')
        with open(filename, 'w') as f:
            dict = day.to_dict()
            dict['week'] = week
            f.write(json.dumps(dict))

    cakefile = os.path.join(CACHE_DIR, f'cake_{week}_{year}.json')
    with open(cakefile, 'w') as f:
        f.write(json.dumps({'cake': cake}))


def read_menu(date: datetime.date):
    filename = os.path.join(CACHE_DIR, f'{date.isoformat()}.json')
    if not os.path.exists(filename):
        return None

    with open(filename, 'r') as f:
        return json.loads(f.read())


def read_cake(week: str, year: str):
    cake_file_path = os.path.join(CACHE_DIR, f"cake_{week}_{year}.json")
    if not os.path.isfile(cake_file_path):
        return None

    with open(cake_file_path, 'r') as f:
        return json.loads(f.read())

