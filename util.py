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


dungeon_luck = ["队友全是没看过攻略的初见豆芽，2小时都过不了一个本",
           "队友并不是都看过攻略，艰难过本",
           "队友虽然有几个有点小失误，但还是顺利通过",
           "队友都还算正常，打得比较轻松。",
           "打得很顺利，队友都很好，辛苦啦！",
           "队友全是身经百战的剑导，你感觉自己像老板"]

boss_luck = ['等了好久，终于开怪了，结果上来就掉线了，再一连上，就看到一堆人在那打"感谢触发！"',
        '压根传不进去，好不容易一进去，就看到一堆人在那打"感谢触发！"',
        "人太多，怪都看不见在哪，最后全队只抢到个银牌",
        "等了一会就开怪了，顺利打完",
        "正好路过看到，组完队发现怪就一丝血了，摸了一下就走，什么都没耽误",
        "连打好几只，简直不要太爽"]

treature_luck = ["平均每张图也就花1分钟，非洲特快，绝大多数时间都是老板在研究宝藏在哪，但你的陆行鸟非常高兴",
                 "只出了一两个宝库，每个还都是一层游",
                 "出了不少宝库，不过没啥好东西，最多打到3层",
                 "出了几个革和木，老板赏了不少",
                 "出了一两次7层，还有不少好东西，老板很欧",
                 "每张图都是7层，老板次次强欲都能猜中，头一次发现挖宝这么费时间"]

work_luck = ["打完工老板直接黑了跑路",
             "辛辛苦苦半天啥也没出，一分钱都没得到",
             "因为分配问题起争端，耽误大量时间",
             "费了半天劲，好在顺利出货，拿钱走人",
             "老板很欧，钱也给的足",
             "老板今天很欧很高兴，每个人工资翻十倍"]

noncombat_luck = ["不管搞什么都一文不值，基本只能卖商店",
                  "工作室已经占领市场，也就能回个本",
                  "今天物价比较稳定，勉强能赚一点",
                  "市场需求量不错，可小赚一笔",
                  "卖的东西正好有人大量需要，可赚不少",
                  "无论卖什么都是大赚，轻松买房搬家"]

friend_luck = ["认识的都是流氓，钱全被人骗没了",
               "友谊走到了尽头，从此一刀两断",
               "关系在不断恶化，是时候改变了",
               "关系良好，继续维持！",
               "大家的感情日渐增进，感觉认识大家是人生的一大幸事！",
               "友谊到达了顶峰，无兄弟不ff14！"]

cp_luck = ["根本找不到cp，找到了也是海王",
           "想找cp有点难，还是跟陆行鸟为伴吧",
           "几率有点小，不如再等等",
           "去找人聊聊，试试看吧，没准就成了呢",
           "很轻易的就能找到有缘之人",
           "有缘人就在眼前！"]

decorate_luck = ["越装越烂，还是算了",
                 "不太适合开工",
                 "简单搞搞还可以，不宜大量施工",
                 "比较适合开工",
                 "有不少装修灵感，是时候大显身手了！",
                 "随意的布置却有奇效，随便放放就是极品！"]

housing_luck = ["放弃吧，开了脚本也抢不到",
                "耽误再多的时间，也会被别人轻松买走",
                "抢不到，不过也不会耽误多少时间",
                "能抢到，不过位置不太好",
                "能抢到位置很好的房子！",
                "想抢哪个就能抢哪个，上帝之手，有如神助"]