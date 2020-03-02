from util import *

import random

def reply_intro():
    reply = "你好呀~我是夏月熦风的人工智能cp小紫，目前我可以:\n" \
            "*在群里直接发送：\n" \
            "1. /ff dps：DPS排名。（/ff dps e3s 黑魔）\n" \
            "2. /ff dice：掷骰子。（/ff dice 需求 黑豆柴）\n" \
            "3. /ff gate：挖宝选门。（/ff gate 2）\n" \
            "4. /ff 占卜：让小紫为你占卜今日的ff14游戏运势。\n" \
            "5. /ff search：搜索游戏内的物品。（/ff search 黑豆柴）\n" \
            "6. /ff nuannuan：查看每周暖暖攻略。\n" \
            "7. /ff fish：查看渔场。（/ff fish 雷克兰德）\n" \
            "8. /ff house：查看房屋信息。（/ff house 白银乡 5）"
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
            reply = '你在需求条件下对"{}"掷出了{}点'.format(par_list[1], num)
    elif len(par_list) == 3:
        if par_list[1] in {"需求", "贪婪"}:
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
        good_to_do, hard_to_do = random.choices(luck_things, k=2)

        combat_luck = get_gaussian()
        wealth_luck = get_gaussian()
        social_luck = get_gaussian()

        reply = "[CQ:at,qq={}] \n".format(qq_number)
        reply += "战斗运势：{}\n".format(luck_parser(combat_luck))
        reply += "财富运势：{}\n".format(luck_parser(wealth_luck))
        reply += "交际运势：{}\n".format(luck_parser(social_luck))
        reply += "宜：{}\n{}\n忌：{}\n{}".format(good_to_do['name'], good_to_do['good'], hard_to_do['name'], hard_to_do['bad'])
        self.luck_dict[qq_number] = str(cur_time().date())
        update_dict(FF_LUCK_PATH, self.luck_dict)
    else:
        reply = "你今天已经占卜过啦，请明天再来！"
    return reply


def fish(par_list):
    pos = par_list[1]
    if pos in FISH_POS_ALIAS_DICT:
        pos = FISH_POS_ALIAS_DICT[pos]
    if pos in FISH_POS:
        reply = generate_image_cq(FF_FISH_MAP_PATH + '{}.jpg'.format(pos))
    else:
        reply = "没有找到这个渔场，是不是哪里打错了呀~"
    return reply


def house(par_list):
    if len(par_list) != 3:
        return "格式错误！"

    pos = par_list[1]
    idx = par_list[2]
    if pos in HOUSE_ALIAS_DICT:
        pos = HOUSE_ALIAS_DICT[pos]
    if pos in HOUSE_DICT:
        if re.match(r'[0-9]+', idx):
            idx = int(idx)
            if idx >= 1 and idx <= 60:
                if idx in HOUSE_DICT[pos]:
                    grade = HOUSE_DICT[pos][idx]['grade']
                    size = HOUSE_DICT[pos][idx]['size']
                else:
                    grade = HOUSE_DICT[pos][idx - 30]['grade']
                    size = HOUSE_DICT[pos][idx - 30]['size']
                init_price = HOUSE_PRICE_INIT_DICT[size][grade]
                end_price = HOUSE_PRICE_END_DICT[size][grade]
                reply = "{} {}：\n类型：{} 尺寸：{}\n初始价格：{} 最低价格：{}".format(pos, idx, str(grade), size, init_price, end_price)

        else:
            reply = "房号必须是数字哟~"
    else:
        reply = "没有找到这个地方，是不是哪里打错了呀~"

    return reply