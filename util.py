from config import *

import re
import json
import os
import random
import datetime


def regex_match(pattern, message):
    if re.match(pattern, message):
        return True
    return False


def load_dict(path):
    if not os.path.exists(path):
        with open(path, 'w+') as f:
            json.dump({}, f)
    with open(path, 'r') as f:
        player_data = json.load(f)
    return player_data


def update_dict(path, dict):
    with open(path, 'w+') as f:
        json.dump(dict, f)


def get_gaussian():
    r = random.normalvariate(0, 1.5)
    if r < -5:
        r = -5
    elif r > 5:
        r = 5
    r = (r + 5) * 10
    r = round(r, 1)
    return r


def luck_parser(num):
    if num <= 7:
        i = 0
    elif num <= 20:
        i = 1
    elif num <= 50:
        i = 2
    elif num <= 80:
        i = 3
    elif num <= 93:
        i = 4
    else:
        i = 5

    return str(num) + "%"


def time_now():
    return datetime.datetime.now() + datetime.timedelta(hours=13)


def done_today(dict, qq_number):
    date = str(time_now().date())
    if qq_number not in dict or dict[qq_number] != date:
        return False
    return True
