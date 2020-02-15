from config import *

import re
import json
import os
import random


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


def luck_parser(num, list):
    if num <= 7:
        return str(num) + "%，" + list[0]
    elif num <= 20:
        return str(num) + "%，" + list[1]
    elif num <= 50:
        return str(num) + "%，" + list[2]
    elif num <= 80:
        return str(num) + "%，" + list[3]
    elif num <= 93:
        return str(num) + "%，" + list[4]
    elif num <= 100:
        return str(num) + "%，" + list[5]