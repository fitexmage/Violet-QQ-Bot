import re
import json
import os
import random
import datetime


def load_all_file():
    with open('data/data.json', 'r') as f:
        data = json.load(f)
    print("All data loaded!")
    return data


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
    return str(num) + "%"


def cur_time():
    return datetime.datetime.now() + datetime.timedelta(hours=13)


def done_today(date):
    cur_date = str(cur_time().date())
    if date == cur_date:
        return True
    return False


def check_ready(last_reply):
    if last_reply is not None and (cur_time() - last_reply).seconds < 10:
        return False
    return True


def generate_image_cq(path):
    return "[CQ:image,file={}]".format(path)


def move_on_earth(lat, lon):
    lat += random.uniform(-2, 2)
    lon += random.uniform(-2, 2)
    if lat > 90:
        lat = 180 - lat
    elif lat < -90:
        lat = -180 - lat

    if lat > 180:
        lat = lat - 360
    elif lat < -180:
        lat = lat + 360
    return lat, lon


def get_name(info):
    if info['card'] != '':
        name = info['card']
    else:
        name = info['nickname']
    return name


def record_duel_info(dict, qq, win):
    cur_date = str(cur_time().date())
    qq = str(qq)
    if qq not in dict or dict[qq]['date'] != cur_date:
        dict[qq] = {'date': cur_date, 'win_times': 0, 'lose_times': 0, 'multi_kill': 0}
    if win:
        dict[qq]['win_times'] += 1
        dict[qq]['multi_kill'] += 1
    else:
        dict[qq]['lose_times'] += 1
        dict[qq]['multi_kill'] = 0
