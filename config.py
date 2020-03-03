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

DUNGEON_DICT = data['dungeon']
DUNGEON_ALIAS_DICT = data['dungeon_alias']
ROLE_DICT = data['role']
ROLE_ALIAS_DICT = data['role_alias']
LEVEL_LIST = data['dps_level']
LUCK_THINGS = data['luck_things']
FISH_POS = data['fish_pos']
FISH_POS_ALIAS_DICT = data['fish_pos_alias']
HOUSE_DICT = data['house']
HOUSE_ALIAS_DICT = data['house_alias']
HOUSE_INIT_PRICE_DICT = data['house_init_price']
HOUSE_END_PRICE_DICT = data['house_end_price']
