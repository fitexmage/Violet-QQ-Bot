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
            "7. /ff fish：查看渔场。（/ff fish 雷克兰德）"
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
        good_to_do = random.choice(luck_things)
        luck_things.remove(good_to_do)
        hard_to_do = random.choice(luck_things)

        combat_luck = get_gaussian()
        wealth_luck = get_gaussian()
        social_luck = get_gaussian()

        reply = "[CQ:at,qq=" + qq_number + "] \n" \
                                           "战斗运势：" + luck_parser(combat_luck) + "\n" \
                                                                                "财富运势：" + luck_parser(
            wealth_luck) + "\n" \
                           "交际运势：" + luck_parser(social_luck) + "\n" \
                                                                "宜：{}  忌：{}".format(good_to_do, hard_to_do)
        self.luck_dict[qq_number] = str(cur_time().date())
        update_dict(FF_LUCK_PATH, self.luck_dict)
    else:
        reply = "你今天已经占卜过啦，请明天再来！"
    return reply


def fish(par_list):
    if par_list[1] in FISH_POS:
        reply = generate_image_cq(
            'file:///Z:\\home\\user\\coolq\\data\\image\\local\\fish_map\\{}.jpg'.format(par_list[1]))
    elif par_list[1] in FISH_MAP_DICT:
        reply = generate_image_cq(
            'file:///Z:\\home\\user\\coolq\\data\\image\\local\\fish_map\\' + FISH_MAP_DICT[par_list[1]]['path'])
    else:
        reply = "没有找到这个渔场，是不是哪里打错了呀~"
    return reply