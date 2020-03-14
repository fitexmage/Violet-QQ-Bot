from util import *
from config import *
from crawler import crawl_dps, crawl_dungeon

import random

def intro():
    reply = "你好呀~我是夏月熦风的人工智能cp小紫，目前我可以:\n" \
            "*在群里直接发送：\n" \
            "1. /ff dps：DPS排名。（/ff dps e3s 黑魔）\n" \
            "2. /ff dice：掷骰子。（/ff dice 需求 黑豆柴）\n" \
            "3. /ff gate：挖宝选门。（/ff gate 2）\n" \
            "4. /ff 占卜：让小紫为你占卜今日的ff14游戏运势。\n" \
            "5. /ff item：搜索游戏内的物品。（/ff item 黑豆柴）\n" \
            "6. /ff dungeon：搜索副本信息。（/ff dungeon 迦楼罗歼灭战）\n" \
            "7. /ff nuannuan：查看每周暖暖攻略。\n" \
            "8. /ff fish：查看渔场。（/ff fish 雷克兰德）\n" \
            "9. /ff house：查看房屋信息。（/ff house 白银乡 5）"
    return reply


def dps(par_list):
    reply = None

    dungeon = par_list[1]
    role = par_list[2]

    if len(par_list) == 3:
        server = "国际服"
    elif len(par_list) == 4:
        server = par_list[3]
    else:
        return reply

    if dungeon in DPS_DUNGEON_NICKNAME_DICT:
        dungeon = DPS_DUNGEON_NICKNAME_DICT[dungeon]

    if role in ROLE_NICKNAME_DICT:
        role = ROLE_NICKNAME_DICT[role]

    if dungeon not in DPS_DUNGEON_DICT or role not in ROLE_DICT:
        return reply

    dps_list = crawl_dps(server, dungeon, role)
    if len(dps_list) != 0:
        reply = '{} {} {}(adps)'.format(DPS_DUNGEON_DICT[dungeon]['name'], role, server)
        for i in range(len(LEVEL_LIST)):
            reply += '\n{}%：{}'.format(LEVEL_LIST[i], dps_list[i])
    else:
        reply = "当前服务器繁忙，请稍候再试！"
    return reply


def dice(par_list):
    reply = None
    num = str(random.randint(1, 99))
    if len(par_list) == 1:
        reply = '你在需求条件下掷出了{}点'.format(num)
    elif len(par_list) == 2:
        if par_list[1] in {"需求", "贪婪"}:
            reply = '你在{}条件下掷出了{}点'.format(par_list[1], num)
        else:
            item = par_list[1]
            if len(item) > 20:
                reply = "你确定有这么长名字的物品吗……"
            else:
                reply = '你在需求条件下对"{}"掷出了{}点'.format(par_list[1], num)
    elif len(par_list) == 3:
        if par_list[1] in {"需求", "贪婪"}:
            item = par_list[1]
            if len(item) > 20:
                reply = "你确定有这么长名字的物品吗……"
            else:
                reply = '你在{}条件下对"{}"掷出了{}点'.format(par_list[1], par_list[2], num)
    return reply


def gate(par_list):
    reply = None
    if par_list[1] == '2':
        if random.random() < 0.9:
            num_1 = str(random.randint(1, 99))
            num_2 = str(random.randint(1, 99))
            reply = "左边门成功的概率是{}%\n右边门成功的概率是{}%".format(num_1, num_2)
        else:
            reply = "别想了，选哪边都没戏~"
    if par_list[1] == '3':
        if random.random() < 0.9:
            num_1 = str(random.randint(1, 99))
            num_2 = str(random.randint(1, 99))
            num_3 = str(random.randint(1, 99))
            reply = "左边门成功的概率是{}%\n中间门成功的概率是{}%\n右边门成功的概率是{}%".format(num_1, num_2, num_3)
        else:
            reply = "别想了，选哪边都没戏~"
    return reply


def luck(self, qq_number):
    if qq_number not in self.luck_dict or not done_today(self.luck_dict[qq_number]):
        good_to_do, hard_to_do = random.sample(LUCK_THINGS, k=2)
        if isinstance(good_to_do['good'], list):
            good = random.choice(good_to_do['good'])
        else:
            good = good_to_do['good']
        if isinstance(hard_to_do['bad'], list):
            bad = random.choice(hard_to_do['bad'])
        else:
            bad = hard_to_do['bad']

        combat_luck = get_gaussian()
        wealth_luck = get_gaussian()
        social_luck = get_gaussian()

        reply = "[CQ:at,qq={}] \n".format(qq_number)
        reply += "战斗运势：{}\n".format(luck_parser(combat_luck))
        reply += "财富运势：{}\n".format(luck_parser(wealth_luck))
        reply += "交际运势：{}\n".format(luck_parser(social_luck))

        reply += "宜：{}\n    {}\n忌：{}\n    {}".format(good_to_do['name'], good, hard_to_do['name'], bad)
        self.luck_dict[qq_number] = str(cur_time().date())
        update_dict(FF_LUCK_PATH, self.luck_dict)
    else:
        reply = "你今天已经占卜过啦，请明天再来！"
    return reply


def dungeon(par_list):
    if len(par_list) > 1:
        dungeon_name = par_list[1]
        if dungeon_name in SEARCH_DUNGEON_NICKNAME_DICT:
            dungeon_name = SEARCH_DUNGEON_NICKNAME_DICT[dungeon_name]
        reply = crawl_dungeon(dungeon_name)
    else:
        reply = "请选择想要查询的副本！"
    return reply


def fish(par_list):
    pos = par_list[1]
    if pos in PLACE_NICKNAME_DICT:
        pos = PLACE_NICKNAME_DICT[pos]
    if pos in PLACE:
        reply = generate_image_cq(FF_FISH_MAP_PATH + '{}.jpg'.format(pos))
    else:
        reply = "没有找到这个渔场，是不是哪里打错了呀~"
    return reply


def house(par_list):
    reply = None
    if len(par_list) != 3:
        return reply

    pos = par_list[1]
    idx = par_list[2]
    if pos in HOUSE_NICKNAME_DICT:
        pos = HOUSE_NICKNAME_DICT[pos]
    if pos in HOUSE_DICT:
        if re.match(r'[0-9]+', idx):
            idx = int(idx)
            if idx >= 1 and idx <= 60:
                if str(idx) in HOUSE_DICT[pos]:
                    grade = HOUSE_DICT[pos][str(idx)]['grade']
                    size = HOUSE_DICT[pos][str(idx)]['size']
                else:
                    grade = HOUSE_DICT[pos][str(idx - 30)]['grade']
                    size = HOUSE_DICT[pos][str(idx - 30)]['size']
                init_price = HOUSE_INIT_PRICE_DICT[size][str(grade)]
                end_price = HOUSE_END_PRICE_DICT[size][str(grade)]
                reply = "{}{}号\n类型：{}      尺寸：{}\n初始价格：{}\n最低价格：{}".format(pos, idx, str(grade), size, init_price, end_price)

        else:
            reply = "房号必须是数字哟~"
    else:
        reply = "没有找到这个地方，是不是哪里打错了呀~"

    return reply