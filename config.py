PLAYER_QQ_PATH = "data/mc_qq.json"
RCON_PASSWORD_PATH = "data/rcon_password.txt"
RAW_URL_PATH = "data/url.csv"
NEW_URL_PATH = "data/new_url.csv"
STOPWORDS_PATH = "data/stopwords.txt"
MC_LUCK_PATH = "data/mc_luck.json"

HOST = "127.0.0.1"  # '192.168.1.3' '172.17.67.53'
PORT = 8080
SELF_QQ_NUMBER = "2511310647"
PARTNER_QQ_NUMBER = "424506920"

SERVER_HOST = "42.51.173.5"
SERVER_PORT = 25565
RCON_PORT = 25575

QUESTION_SET = ["Mod讨论", "游戏技巧", "编程开发", "联机教程", "Mod教程", "Mod问答", "联机问答", "原版问答", "矿工茶馆"]

########################
WIKI_URL = "https://ff14.huijiwiki.com/wiki/"
NUANNUAN_URL = "http://nuannuan.yorushika.co:5000/"

FF_LUCK_PATH = "data/ff_luck.json"

IP_DICT = {'ff14': {'name': '最终幻想14', 'ip': '116.211.8.38'},
           '最终幻想14': {'name': '最终幻想14', 'ip': '116.211.8.38'}}

DUNGEON_DICT = {'e1': {'name': '普通至尊伊甸', 'attr': '29#boss=65&difficulty=100'},
                'e2': {'name': '普通虚空行者', 'attr': '29#boss=66&difficulty=100'},
                'e3': {'name': '普通利威亚桑', 'attr': '29#boss=67&difficulty=100'},
                'e4': {'name': '普通泰坦', 'attr': '29#boss=68&difficulty=100'},
                'e1s': {'name': '零式虚空行者', 'attr': '29#boss=65&difficulty=101'},
                'e2s': {'name': '零式虚空行者', 'attr': '29#boss=66&difficulty=101'},
                'e3s': {'name': '零式利威亚桑', 'attr': '29#boss=67&difficulty=101'},
                'e4s': {'name': '零式泰坦', 'attr': '29#boss=67&difficulty=101'}
                }

ROLE_DICT = {'占星术士': {'name': '占星术士', 'attr': 'Astrologian'},
             '占星': {'name': '占星术士', 'attr': 'Astrologian'},
             '吟游诗人': {'name': '吟游诗人', 'attr': 'Bard'},
             '诗人': {'name': '吟游诗人', 'attr': 'Bard'},
             '黑魔法师': {'name': '黑魔法师', 'attr': 'BlackMage'},
             '黑魔': {'name': '黑魔法师', 'attr': 'BlackMage'},
             '舞者': {'name': '舞者', 'attr': 'Dancer'},
             '暗黑骑士': {'name': '暗黑骑士', 'attr': 'DarkKnight'},
             '黑骑': {'name': '暗黑骑士', 'attr': 'DarkKnight'},
             'DK': {'name': '暗黑骑士', 'attr': 'DarkKnight'},
             '龙骑士': {'name': '龙骑士', 'attr': 'Dragoon'},
             '龙骑': {'name': '龙骑士', 'attr': 'Dragoon'},
             '绝枪战士': {'name': '绝枪战士', 'attr': 'Gunbreaker'},
             '绝枪': {'name': '绝枪战士', 'attr': 'Gunbreaker'},
             '机工士': {'name': '机工士', 'attr': 'Machinist'},
             '机工': {'name': '机工士', 'attr': 'Machinist'},
             '武僧': {'name': '武僧', 'attr': 'Monk'},
             '忍者': {'name': '忍者', 'attr': 'Ninja'},
             '骑士': {'name': '骑士', 'attr': 'Paladin'},
             '赤魔法师': {'name': '赤魔法师', 'attr': 'RedMage'},
             '赤魔': {'name': '赤魔法师', 'attr': 'RedMage'},
             '武士': {'name': '武士', 'attr': 'Samurai'},
             '学者': {'name': '学者', 'attr': 'Scholar'},
             '召唤师': {'name': '召唤师', 'attr': 'Summoner'},
             '召唤': {'name': '召唤师', 'attr': 'Summoner'},
             '战士': {'name': '战士', 'attr': 'Warrior'},
             '白魔法师': {'name': '白魔法师', 'attr': 'WhiteMage'},
             '白魔': {'name': '白魔法师', 'attr': 'WhiteMage'}
             }

LEVEL_DICT = {0: '100%',
              1: '99%',
              2: '95%',
              3: '75%',
              4: '50%',
              5: '25%',
              6: '10%'}

luck_things = ['4人本', '8人本', '24人本', '主线本', '南方堡', '动画城', '带豆芽打本', '吃宝宝', '导随', '练级', 'fate',
               '刷成就', '刷双色宝石', '古武', '魂武', 'ULK', 'PVP', '跟狩猎车', '打S怪', '抢开', '野外BOSS',
               '刷神典石', '刷素材', '刷钱', '刷幻化', '刷坐骑', '筹备', '理符', '收藏品', '刷黄票', '刷白票',
               '采集', '制作', '挖宝', '打工', '板子PVP', '压价', '钓鱼',
               '金蝶', '跳跳乐', '喷风', '仙人彩', '仙人微彩', '暖暖', '赛鸟', '萌宠之王', '九宫幻卡', '金蝶小游戏',
               '交友', '友尽', '换部队', '退部队', '参加部队活动', '找CP', '换CP', '当海王', '当舔狗', '偷晴', '捡豆芽', '演奏',
               '去RP店', '找牛郎', '参加大型活动', '装修', '抢房', '幻化', '理发', '洗澡', '给雇员洗澡', '看风景', '登录游戏']

FISH_POS = {'黑衣森林东部林区', '阿巴拉提亚云海', '魔大陆阿济兹拉', '雷克兰德', '库尔札斯中央高地', '黑衣森林南部林区', '黑风海', '摩杜纳', '基拉巴尼亚湖区', '中拉诺西亚', '西拉诺西亚', '安穆·艾兰', '伊尔美格', '龙堡参天高地', '基拉巴尼亚山区', '黑衣森林北部林区', '中萨纳兰', '东拉诺西亚', '北萨纳兰', '格里达尼亚新街', '格里达尼亚旧街', '延夏', '神拳痕', '基拉巴尼亚边区', '库尔札斯西部高地', '翻云雾海', '拉诺西亚高地', '黑衣森林中央林区', '白银乡', '水晶都', '南萨纳兰', '龙堡内陆低地', '太阳神草原', '珂露西亚岛', '西萨纳兰', '红玉海', '东萨纳兰', '拉凯提卡大森林', '拉诺西亚外地', '拉诺西亚低地'}

FISH_MAP_DICT = {'东拉': {'name': '东拉诺西亚', 'path': '东拉诺西亚.jpg'},
                 '东萨': {'name': '东萨纳兰', 'path': '东萨纳兰.jpg'},
                 '中拉': {'name': '中拉诺西亚', 'path': '中拉诺西亚.jpg'},
                 '中萨': {'name': '中萨纳兰', 'path': '中萨纳兰.jpg'},
                 '北萨': {'name': '北萨纳兰', 'path': '北萨纳兰.jpg'},
                 '南萨': {'name': '南萨纳兰', 'path': '南萨纳兰'},
                 '山区': {'name': '基拉巴尼亚山区', 'path': '基拉巴尼亚山区.jpg'},
                 '湖区': {'name': '基拉巴尼亚湖区', 'path': '基拉巴尼亚湖区.jpg'},
                 '边区': {'name': '基拉巴尼亚边区', 'path': '基拉巴尼亚边区.jpg'},
                 '中高': {'name': '库尔札斯中央高地', 'path': '库尔札斯中央高地.jpg'},
                 '西高': {'name': '库尔札斯西部高地', 'path': '库尔札斯西部高地.jpg'},
                 '大森林': {'name': '拉凯提卡大森林', 'path': '拉凯提卡大森林.jpg'},
                 '拉低': {'name': '拉诺西亚低地', 'path': '拉诺西亚低地.jpg'},
                 '拉外': {'name': '拉诺西亚外地', 'path': '拉诺西亚外地.jpg'},
                 '拉高': {'name': '拉诺西亚高地', 'path': '拉诺西亚高地.jpg'},
                 '魔都': {'name': '摩杜纳', 'path': '摩杜纳.jpg'},
                 '西拉': {'name': '西拉诺西亚', 'path': '西拉诺西亚.jpg'},
                 '西萨': {'name': '西萨纳兰', 'path': '西萨纳兰.jpg'},
                 '云海': {'name': '阿巴拉提亚云海', 'path': '阿巴拉提亚云海.jpg'},
                 '魔大陆': {'name': '魔大陆阿济兹拉', 'path': '魔大陆阿济兹拉.jpg'},
                 '东森': {'name': '黑衣森林东部林区', 'path': '黑衣森林东部林区.jpg'},
                 '中森': {'name': '黑衣森林中部林区', 'path': '黑衣森林中部林区.jpg'},
                 '北森': {'name': '黑衣森林北部林区', 'path': '黑衣森林北部林区.jpg'},
                 '南森': {'name': '黑衣森林南部林区', 'path': '黑衣森林南部林区.jpg'},
                 '龙低': {'name': '龙堡内陆低地', 'path': '龙堡内陆低地.jpg'},
                 '龙高': {'name': '龙堡参天高地', 'path': '龙堡参天高地.jpg'},
                 }

##############################
DUEL_PATH = "data/duel.json"

multi_kill = {3: "正在大杀特杀！",
              4: "已经接近暴走了！",
              5: "已经无人能挡了！",
              6: "已经主宰比赛了！",
              7: "已经接近神了！",
              8: "已经超越腐竹了！"}