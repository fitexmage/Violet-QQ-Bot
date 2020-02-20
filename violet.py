from util import *
from crawler import *
from mc_system import MC_System
from ff_system import FF_System

import os

class Violet:
    def __init__(self):
        self.enable = True
        self.debug = False
        self.cur_lat = random.uniform(-90, 90)
        self.cur_lon = random.uniform(-180, 180)

        self.duel_dict = load_dict(DUEL_PATH)

        self.mc_system = MC_System()
        self.ff_ststem = FF_System()

    def reply_intro(self):
        reply = "你好呀~我是某人的人工智能搭档小紫，目前我的辅助范围有:\n" \
                "1. MC影之乡服务器。（发送\"/mc help\"获取详情）\n" \
                "2. 最终幻想14。（发送\"/ff help\"获取详情）"
        return reply

    def reply_private_msg(self, context):
        message = context['message']

        reply = None

        if self.enable:
            if message == "你好":
                reply = "你好呀~"

            if reply is None:
                reply = self.mc_system.reply_private_msg(context)

            if reply is None:
                reply = self.ff_ststem.reply_private_msg(context)

        return reply

    async def reply_group_msg(self, bot, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = None

        if random.random() < 0.05:
            reply = random.choice(["是的呀", "我也觉得是~", "没错", "哈哈哈", "嗯嗯"])

        if qq_number == PARTNER_QQ_NUMBER:
            if message == "小紫 启":
                reply = self.start()
            elif message == "小紫 散":
                reply = self.close()

        if self.enable:
            if message == "小紫" or message == "@【影之接待】小紫" or message == "[CQ:at,qq=" + SELF_QQ_NUMBER + "] ":
                reply = self.reply_intro()

            elif regex_match('\\[CQ:at,qq={}\\].*'.format(SELF_QQ_NUMBER), message):
                reply = self.reply_group_at_msg(context, message, qq_number)

            elif regex_match('^/', message):
                reply = await self.reply_group_cmd_msg(bot, context, message)

        return reply

    def reply_group_at_msg(self, context, message, qq_number):
        at_content = re.match('\\[CQ:at,qq={}\\](.*)'.format(SELF_QQ_NUMBER), message).group(1).strip()

        reply = None

        if self.debug:
            print("Context: " + at_content)
        elif regex_match("你是谁", at_content):
            reply = "我是小紫呀~"
        elif at_content == "我爱你":
            if qq_number == PARTNER_QQ_NUMBER:
                reply = "我也爱你呀~"
            else:
                reply = "我不是那么随便的人~"
        elif regex_match('连接.+', at_content):
            name = re.match('连接(.+)', at_content).group(1)
            if name in IP_DICT:
                backinfo = os.system('ping -c 1 -W 1 %s' % IP_DICT[name]['ip'])
                if backinfo == 0:
                    reply = IP_DICT[name]['name'] + "服务器连接良好"
                else:
                    reply = IP_DICT[name]['name'] + "服务器连接失败"
            else:
                reply = "未记录此服务器信息！"
        elif at_content == "服务器时间":
            reply = "现在的时间是：{}".format(str(cur_time()).split('.')[0])
        elif re.match('你在哪', at_content):
            self.cur_lat, self.cur_lon = move_on_earth(self.cur_lat, self.cur_lon)
            lat = str(round(self.cur_lat, 6))
            lon = str(round(self.cur_lon, 6))
            reply = ["[CQ:location,lat={},lon={}]".format(lat, lon), "来找我玩呀~"]
        elif at_content == "debug":
            if qq_number == PARTNER_QQ_NUMBER:
                self.debug = not self.debug
                reply = "Debug模式已更换为：{}！".format(str(self.debug))

        if reply is None:
            reply = self.mc_system.reply_group_at_msg(context, at_content)
        if reply is None:
            reply = self.ff_ststem.reply_group_at_msg(context, at_content)
        return reply

    async def reply_group_cmd_msg(self, bot, context, message):
        command = message[1:]
        par_list = command.split(' ')

        reply = None

        if par_list[0] == 'duel':
            if len(par_list) == 1 or par_list[1] == "":
                reply = "请选择一位对手吧！"
            elif par_list[1] == "record":
                self_qq = context['user_id']
                if self_qq not in self.duel_dict or not done_today(self.duel_dict[self_qq]['date']):
                    win_times = 0
                    lose_times = 0
                else:
                    win_times = self.duel_dict[self_qq]['win_times']
                    lose_times = self.duel_dict[self_qq]['lose_times']
                reply = "你今日决斗的战绩为：{}胜，{}负~".format(win_times, lose_times)
            elif par_list[1] == "rank":
                record_list = []
                for qq in self.duel_dict:
                    if done_today(self.duel_dict[qq]['date']) and self.duel_dict[qq]['win_times'] > 0:
                        record_list.append((qq, self.duel_dict[qq]['win_times'] / (self.duel_dict[qq]['win_times'] + self.duel_dict[qq]['lose_times'])))
                if len(record_list) == 0:
                    reply = "今天还没有人决斗过哦，过来试试吧~"
                else:
                    record_list.sort(key=lambda k: k[1], reverse=True)
                    reply = "下面是今日的决斗胜率榜，今天你上榜了嘛~\n"
                    for i in range(min(len(record_list), 5)):
                        reply += "{}. {} {}%\n".format(str(i+1), record_list[i][0], round(record_list[i][1] * 100, 2))
                    reply = reply.strip()
            else:
                self_qq = str(context['user_id'])
                opponent_qq = par_list[1]

                if self_qq == opponent_qq:
                    reply = "你想自残吗……"
                else:
                    try:
                        self_info = await bot.get_group_member_info(group_id=int(context['group_id']), user_id=int(self_qq))
                        opponent_info = await bot.get_group_member_info(group_id=int(context['group_id']), user_id=int(opponent_qq))
                        if self_qq == PARTNER_QQ_NUMBER and opponent_qq == SELF_QQ_NUMBER:
                            reply = "不急，等晚上再一起玩~"
                        elif self_info['role'] == 'admin' or self_info['role'] == 'owner':
                            if opponent_info['role'] == "admin" or opponent_info['role'] == "owner":
                                reply = "管理员之间的争斗，我管不了……"
                            else:
                                await bot.set_group_ban(group_id=context['group_id'], user_id=str(opponent_qq), duration=10 * 60)
                                reply = "一股强大的力量袭来……"
                        elif opponent_info['role'] == "owner":
                            await bot.set_group_ban(group_id=context['group_id'], user_id=str(self_qq), duration=15 * 60)
                            reply = "竟敢挑战群主，你将受到天罚！"
                        elif str(opponent_info['user_id']) == SELF_QQ_NUMBER:
                            await bot.set_group_ban(group_id=context['group_id'], user_id=str(self_qq), duration=15 * 60)
                            reply = "我定的规则，你觉得我会输吗~"
                        elif opponent_info['role'] == "admin":
                            await bot.set_group_ban(group_id=context['group_id'], user_id=str(self_qq), duration=15 * 60)
                            reply = "竟敢挑战管理员，你将受到天罚！"
                        elif random.random() < 0.5:
                            await bot.set_group_ban(group_id=context['group_id'], user_id=str(self_qq), duration=10 * 60)
                            self_name = get_name(self_info)
                            opponent_name = get_name(opponent_info)
                            reply = "{} VS {}\n你在决斗中失败了……".format(self_name, opponent_name)
                            record_duel_info(self.duel_dict, self_qq, False)
                            record_duel_info(self.duel_dict, opponent_qq, True)
                            update_dict(DUEL_PATH, self.duel_dict)
                        else:
                            await bot.set_group_ban(group_id=context['group_id'], user_id=str(opponent_qq), duration=10 * 60)
                            self_name = get_name(self_info)
                            opponent_name = get_name(opponent_info)
                            reply = "{} VS {}\n你在决斗中胜利了！".format(self_name, opponent_name)
                            record_duel_info(self.duel_dict, self_qq, True)
                            record_duel_info(self.duel_dict, opponent_qq, False)
                            update_dict(DUEL_PATH, self.duel_dict)
                    except:
                        reply = "群里貌似并没有这个人……"


        elif par_list[0] == 'mc' and len(par_list) > 1:
            reply = self.mc_system.reply_group_cmd_msg(context, par_list[1:])

        elif par_list[0] == 'ff' and len(par_list) > 1:
            reply = self.ff_ststem.reply_group_cmd_msg(context, par_list[1:])
        return reply

    def start(self):
        self.enable = True
        reply = "小紫已启动"
        return reply

    def close(self):
        self.enable = False
        reply = "小紫已关闭"
        return reply
