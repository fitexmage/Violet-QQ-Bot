from config import *
from util import *
from crawler import crawl_combat_data, crawl_item

import random

class FF_System:
    def __init__(self):
        self.luck_dict = load_dict(ff_luck_path)

    def reply_intro(self):
        reply = "你好呀~我是夏月熦风的人工智能cp小紫，目前我可以:\n" \
                "1. /ff dps：DPS排名。（/dps e3s 黑魔）\n" \
                "2. /ff 占卜：让小紫为你占卜今日的ff14游戏运势。\n" \
                "3. /ff dice：掷骰子（/dice 需求 黑豆柴）。\n" \
                "4. /ff gate：挖宝选门。（/gate 1）\n"
        return reply

    def reply_private_msg(self, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = None

        return reply

    def reply_group_at_msg(self, context, at_content):
        qq_number = str(context['sender']['user_id'])

        reply = None

        return reply

    def reply_group_cmd_msg(self, context, command):
        qq_number = str(context['sender']['user_id'])

        reply = None

        if regex_match('^dps .+', command):
            reply = crawl_combat_data(command)
        elif regex_match('^dice.+', command):
            par_list = command.split(' ')
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
        elif regex_match('^gate .+', command):
            par_list = command.split(' ')
            if par_list[1] in {'1', '2', '3', '4', '5', '6', '7'}:
                if random.random() < 0.9:
                    num_1 = str(random.randint(1, 99))
                    num_2 = str(random.randint(1, 99))
                    reply = "左边门成功的概率是{}, 右边门成功的概率是{}".format(num_1, num_2)
                else:
                    reply = "别想了，选哪边都没戏~"
        elif command == '占卜':
            reply = "下面是小紫采用人工智能秘术所做出的占卜：\n" \
                    "1. 战斗运势：\n" \
                    "打本：" + luck_parser(random.randint(0, 100), dungeon_luck) + "\n" \
                    "野外BOSS：" + luck_parser(random.randint(0, 100), boss_luck) + "\n" \
                    "2. 财富运势：\n" \
                    "挖宝：" + luck_parser(random.randint(0, 100), treature_luck) + "\n" \
                    "打工：" + luck_parser(random.randint(0, 100), work_luck) + "\n" \
                    "生产采集：" + luck_parser(random.randint(0, 100), noncombat_luck) + "\n" \
                    "3. 交际运势：\n" \
                    "交友：" + luck_parser(random.randint(0, 100), friend_luck) + "\n" \
                    "找CP：" + luck_parser(random.randint(0, 100), cp_luck) + "\n" \
                    "装修：" + luck_parser(random.randint(0, 100), decorate_luck) + "\n" \
                    "抢房：" + luck_parser(random.randint(0, 100), housing_luck)
        elif regex_match('^search .+', command):
            par_list = command.split(' ')
            item = par_list[1]
            reply = crawl_item(item)

        elif command == 'ghs':
            reply = "下面是转自我cp夏月熦风的话：搞搞搞，搞nmb"

        return reply
