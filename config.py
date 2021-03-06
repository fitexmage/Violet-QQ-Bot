from util import *

data = load_all_file()
config = load_all_config()

HOST = "127.0.0.1"  # '192.168.1.3' '172.17.67.53'
PORT = 8080
SELF_QQ = config['self_qq']
PARTNER_QQ = config['partner_qq']
SHADOWVILLAGE_QQ = config['shadowvillage_qq']

TIMEFORMAT_YMDHMS = "%Y-%m-%d %H:%M:%S"


################################################

AVATAR_PATH = "file:///Z:\\home\\user\\coolq\\data\\image\\local\\avatar\\"
CHAT_DATA_DIR_PATH = "data/chat_data/"
DUEL_PATH = "data/duel.json"

ZHIDAO_URL = "https://zhidao.baidu.com/search?word="
BAIKE_URL = "https://baike.baidu.com/item/"
IMAGE_URL = "http://image.so.com/j?"
NETEASE_MUSIC_URL = "http://musicapi.leanapp.cn/search?keywords="

MULTI_KILL = data['multi_kill']

################################################

PLAYER_QQ_PATH = "data/mc_qq.json"
RAW_URL_PATH = "data/url.csv"
NEW_URL_PATH = "data/new_url.csv"
STOPWORDS_PATH = "data/stopwords.txt"
MC_LUCK_PATH = "data/mc_luck.json"

RCON_PASSWORD = config['rcon_password']
SERVER_HOST = "42.51.173.5"
SERVER_PORT = 25565
RCON_PORT = 25575

# QUESTION_SET = ["Mod讨论", "游戏技巧", "编程开发", "联机教程", "Mod教程", "Mod问答", "联机问答", "原版问答", "矿工茶馆"]

################################################
WIKI_URL = "https://ff14.huijiwiki.com/wiki/"
NUANNUAN_URL = "http://nuannuan.yorushika.co:5000/"
FFLOGS_URL = "https://www.fflogs.com"
HERO_LIST_URL = "http://act.ff.sdo.com/20180525HeroList/index200305.html"

FF_LUCK_PATH = "data/ff_luck.json"
FF_FISH_MAP_PATH = "file:///Z:\\home\\user\\coolq\\data\\image\\local\\fish_map\\"

DPS_DUNGEON_DICT = data['dps_dungeon']
DPS_DUNGEON_NICKNAME_DICT = data['dps_dungeon_nickname']
ROLE_DICT = data['role']
ROLE_NICKNAME_DICT = data['role_nickname']
SEARCH_DUNGEON_DICT = data['search_dungeon']
SEARCH_DUNGEON_NICKNAME_DICT = data['search_dungeon_nickname']
SERVER_DICT = data['server']
SERVER_NICKNAME_DICT = data['server_nickname']
WORLD_DICT = data['world']
UNIVERSALIS_ID_dict = data['universalis_id']
LEVEL_LIST = data['dps_level']
LUCK_THINGS = data['luck_things']
PLACE = data['place']
PLACE_NICKNAME_DICT = data['place_nickname']
HOUSE_DICT = data['house']
HOUSE_NICKNAME_DICT = data['house_nickname']
HOUSE_INIT_PRICE_DICT = data['house_init_price']
HOUSE_END_PRICE_DICT = data['house_end_price']
