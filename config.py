from util import *

HOST = "127.0.0.1"  # '192.168.1.3' '172.17.67.53'
PORT = 8080
SELF_QQ_NUMBER = "2511310647"
PARTNER_QQ_NUMBER = "424506920"
SHADOWVILLAGE_QQ_NUMBER = "298466962"

data = load_all_file()

################################################

DUEL_PATH = "data/duel.json"

MULTI_KILL = data['multi_kill']

################################################

PLAYER_QQ_PATH = "data/mc_qq.json"
RCON_PASSWORD_PATH = "data/rcon_password.txt"
RAW_URL_PATH = "data/url.csv"
NEW_URL_PATH = "data/new_url.csv"
STOPWORDS_PATH = "data/stopwords.txt"
MC_LUCK_PATH = "data/mc_luck.json"

SERVER_HOST = "42.51.173.5"
SERVER_PORT = 25565
RCON_PORT = 25575

# QUESTION_SET = ["Mod讨论", "游戏技巧", "编程开发", "联机教程", "Mod教程", "Mod问答", "联机问答", "原版问答", "矿工茶馆"]

################################################
WIKI_URL = "https://ff14.huijiwiki.com/wiki/"
NUANNUAN_URL = "http://nuannuan.yorushika.co:5000/"
FFLOGS_URL = "https://www.fflogs.com"

FF_LUCK_PATH = "data/ff_luck.json"
FF_FISH_MAP_PATH = "file:///Z:\\home\\user\\coolq\\data\\image\\local\\fish_map\\"

def load_dps_dungeon_nickname():
    nickname_dict = {}

    for dungeon in DPS_DUNGEON_DICT:
        if 'nickname' in DPS_DUNGEON_DICT[dungeon]:
            for nickname in DPS_DUNGEON_DICT[dungeon]['nickname']:
                nickname_dict[nickname] = dungeon
    return nickname_dict

def load_role_nickname():
    nickname_dict = {}

    for role in ROLE_DICT:
        if 'nickname' in ROLE_DICT[role]:
            for nickname in ROLE_DICT[role]['nickname']:
                nickname_dict[nickname] = role
    return nickname_dict

def load_search_dungeon_nickname():
    nickname_dict = {}

    for dungeon in SEARCH_DUNGEON_DICT:
        for nickname in SEARCH_DUNGEON_DICT[dungeon]:
            nickname_dict[nickname] = dungeon
    return nickname_dict


def load_fish_pos_nickname():
    nickname_dict = {}

    for place in FISH_POS:
        for nickname in FISH_POS[place]:
            nickname_dict[nickname] = place
    return nickname_dict


DPS_DUNGEON_DICT = data['dps_dungeon']
DPS_DUNGEON_NICKNAME_DICT = load_dps_dungeon_nickname()
ROLE_DICT = data['role']
ROLE_NICKNAME_DICT = load_role_nickname()
SEARCH_DUNGEON_DICT = data['search_dungeon']
SEARCH_DUNGEON_NICKNAME_DICT = load_search_dungeon_nickname()
LEVEL_LIST = data['dps_level']
LUCK_THINGS = data['luck_things']
FISH_POS = data['place']
FISH_POS_NICKNAME_DICT = load_fish_pos_nickname()
HOUSE_DICT = data['house']
HOUSE_NICKNAME_DICT = data['house_nickname']
HOUSE_INIT_PRICE_DICT = data['house_init_price']
HOUSE_END_PRICE_DICT = data['house_end_price']
