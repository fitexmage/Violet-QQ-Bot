from config import *

import re


def regex_match(pattern, message):
    if re.match(pattern, message):
        return True
    return False


def load_player_qq():
    with open(player_qq_path, 'r') as f:
        player_infos = f.read().splitlines()

    player_qq_dict = {}
    for player_info in player_infos:
        info = player_info.split(" ")
        player_qq_dict[info[0]] = info[1]
    return player_qq_dict