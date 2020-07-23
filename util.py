import re
import json
import os
import random
import datetime


def load_dps_dungeon_nickname(data):
    nickname_dict = {}

    for dungeon in data['dps_dungeon']:
        if 'nickname' in data['dps_dungeon'][dungeon]:
            for nickname in data['dps_dungeon'][dungeon]['nickname']:
                nickname_dict[nickname] = dungeon
    return nickname_dict


def load_role_nickname(data):
    nickname_dict = {}

    for role in data['role']:
        if 'nickname' in data['role'][role]:
            for nickname in data['role'][role]['nickname']:
                nickname_dict[nickname] = role
    return nickname_dict


def load_search_dungeon_nickname(data):
    nickname_dict = {}

    for dungeon in data['search_dungeon']:
        for nickname in data['search_dungeon'][dungeon]:
            nickname_dict[nickname] = dungeon
    return nickname_dict


def load_server_nickname(data):
    nickname_dict = {}

    for server in data['server']:
        for nickname in data['server'][server]['nickname']:
            nickname_dict[nickname] = server
    return nickname_dict


def load_universalis_id(data):
    id_dict = {}

    for server in data['world']:
        id_dict[data['world'][server]['universalis_id']] = server

    return id_dict


def load_place_nickname(data):
    nickname_dict = {}

    for place in data['place']:
        for nickname in data['place'][place]:
            nickname_dict[nickname] = place
    return nickname_dict


def load_house_nickname(data):
    nickname_dict = {}

    for place in data['house']:
        for nickname in data['house'][place]['nickname']:
            nickname_dict[nickname] = place
    return nickname_dict


def load_all_file():
    with open('data/data.json', 'r') as f:
        data = json.load(f)
    data['dps_dungeon_nickname'] = load_dps_dungeon_nickname(data)
    data['role_nickname'] = load_role_nickname(data)
    data['search_dungeon_nickname'] = load_search_dungeon_nickname(data)
    data['place_nickname'] = load_place_nickname(data)
    data['house_nickname'] = load_house_nickname(data)
    data['server_nickname'] = load_server_nickname(data)
    data['universalis_id'] = load_universalis_id(data)
    print("All data loaded!")
    return data


def load_all_config():
    with open('data/config.json', 'r') as f:
        config = json.load(f)
    return config


def regex_match(pattern, message):
    if re.match(pattern, message):
        return True
    return False


def load_file(path, type=dict):
    if not os.path.exists(path):
        with open(path, 'w+') as f:
            json.dump(type(), f)
    with open(path, 'r') as f:
        player_data = json.load(f)
    return player_data


def update_file(path, file):
    with open(path, 'w+') as f:
        json.dump(file, f, ensure_ascii=False)


def get_gaussian():
    r = random.normalvariate(0, 2.5)
    if r < -5:
        r = -5
    elif r > 5:
        r = 5
    r = (r + 5) * 10
    r = round(r, 1)
    return r


def luck_parser(num):
    return str(num) + "%"


def cur_time():
    return datetime.datetime.now() + datetime.timedelta(hours=12)


def done_today(date):
    cur_date = str(cur_time().date())
    if date == cur_date:
        return True
    return False


def check_ready(last_reply):
    if last_reply is not None and (cur_time() - last_reply).seconds < 30:
        return False
    return True


def generate_image_cq(path):
    return "[CQ:image,file={}]".format(path)


def generate_music_cq(id, type):
    return "[CQ:music,id={},type={}]".format(id, type)


def get_name(info):
    if info['card'] != '':
        name = info['card']
    else:
        name = info['nickname']
    return name
