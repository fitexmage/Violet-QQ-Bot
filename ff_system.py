from config import *
from util import *
from crawler import crawl_combat_data, crawl_item

import random
import datetime
import requests
import json


class FF_System:
    def __init__(self):
        self.luck_dict = load_dict(FF_LUCK_PATH)

    def reply_intro(self):
        reply = "你好呀~我是夏月熦风的人工智能cp小紫，目前我可以:\n" \
                "*在群里直接发送：\n" \
                "1. /ff dps：DPS排名。（/ff dps e3s 黑魔）\n" \
                "2. /ff dice：掷骰子。（/ff dice 需求 黑豆柴）\n" \
                "3. /ff gate：挖宝选门。（/ff gate 1）\n" \
                "4. /ff 占卜：让小紫为你占卜今日的ff14游戏运势。\n" \
                "5. /ff search：搜索游戏内的物品。（/ff search 黑豆柴）\n" \
                "6. /ff nuannuan：查看每周暖暖攻略。"
        return reply

    def reply_private_msg(self, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = None

        return reply

    def reply_group_at_msg(self, context, at_content):
        qq_number = str(context['sender']['user_id'])

        reply = None

        if at_content in {"最终幻想14", "ff14"}:
            reply = self.reply_intro()

        return reply

    def reply_group_cmd_msg(self, context, command):
        qq_number = str(context['sender']['user_id'])

        reply = None

        if command == 'help':
            reply = self.reply_intro()

        elif regex_match('^dps .+', command):
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
                    reply = "左边门成功的概率是{}%, 右边门成功的概率是{}%".format(num_1, num_2)
                else:
                    reply = "别想了，选哪边都没戏~"

        elif command == '占卜':
            date = str(datetime.date.today())
            if qq_number not in self.luck_dict or self.luck_dict[qq_number] != date:
                reply = "下面是小紫采用人工智能秘术所做出的占卜：\n" \
                        "1. 战斗运势：\n" \
                        "打本：" + luck_parser(get_gaussian(), dungeon_luck) + "\n" \
                        "野外BOSS：" + luck_parser(get_gaussian(), boss_luck) + "\n\n" \
                        "2. 财富运势：\n" \
                        "挖宝：" + luck_parser(get_gaussian(), treature_luck) + "\n" \
                        "打工：" + luck_parser(get_gaussian(), work_luck) + "\n" \
                        "生产采集：" + luck_parser(get_gaussian(), noncombat_luck) + "\n\n" \
                        "3. 交际运势：\n" \
                        "交友：" + luck_parser(get_gaussian(), friend_luck) + "\n" \
                        "找CP：" + luck_parser(get_gaussian(), cp_luck) + "\n" \
                        "装修：" + luck_parser(get_gaussian(), decorate_luck) + "\n" \
                        "抢房：" + luck_parser(get_gaussian(), housing_luck)
                self.luck_dict[qq_number] = date
                update_dict(FF_LUCK_PATH, self.luck_dict)
            else:
                reply = "你今天已经占卜过啦，请明天再来！"

        elif regex_match('^search .+', command):
            par_list = command.split(' ')
            item = par_list[1]
            reply = crawl_item(item)

        elif command == 'nuannuan':
            url = 'http://nuannuan.yorushika.co:5000/'
            r = requests.get(url=url, timeout=5)
            data = json.loads(r.text)
            if data['success']:
                reply = data['content']
            else:
                reply = "暖暖崩了，请稍候再试~"

        elif command == 'ghs':
            reply = "群里的群员都可以搞哟~"

        return reply


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
                 "出了几个宝库，不过没啥好东西，最多打到3层",
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