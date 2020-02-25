from config import *
from util import *

import re
import os


def reply_intro():
    reply = "你好呀~我是某人的人工智能搭档小紫，目前我的辅助范围有:\n" \
            "1. MC影之乡服务器。（发送\"/mc help\"获取详情）\n" \
            "2. 最终幻想14。（发送\"/ff help\"获取详情）"
    return reply


def who_r_u():
    reply = "我是小紫呀~"
    return reply


def i_love_u(qq_number):
    if qq_number == PARTNER_QQ_NUMBER:
        reply = "我也爱你呀~"
    else:
        reply = "我不是那么随便的人~"
    return reply


def connect_server(at_content):
    name = re.match('连接(.+)', at_content).group(1)
    backinfo = os.system('ping -c 1 -W 1 ' + name)
    if backinfo == 0:
        reply = "服务器连接良好"
    else:
        reply = "服务器连接失败"
    return reply


def server_time():
    reply = "现在的时间是：{}".format(str(cur_time()).split('.')[0])
    return reply


def where_r_u(self):
    self.cur_lat, self.cur_lon = move_on_earth(self.cur_lat, self.cur_lon)
    lat = str(round(self.cur_lat, 6))
    lon = str(round(self.cur_lon, 6))
    reply = ["[CQ:location,lat={},lon={}]".format(lat, lon), "来找我玩呀~"]
    return reply


async def duel(self, bot, context, par_list):
    group_id = str(context['group_id'])
    self_qq = str(context['user_id'])

    if group_id not in self.duel_dict:
        self.duel_dict[group_id] = {}

    if len(par_list) == 1 or par_list[1] == "":
        reply = "请选择一位对手吧！"
    elif par_list[1] == "record":
        reply = duel_record(self, group_id, self_qq)
    elif par_list[1] == "rank":
        reply = duel_rank(self, group_id)
    else:
        opponent_qq = par_list[1]
        reply = await duel_qq(self, bot, group_id, self_qq, opponent_qq)

    return reply


def duel_record(self, group_id, self_qq):
    if self_qq not in self.duel_dict[group_id] or not done_today(self.duel_dict[group_id][self_qq]['date']):
        win_times = 0
        lose_times = 0
    else:
        win_times = self.duel_dict[group_id][self_qq]['win_times']
        lose_times = self.duel_dict[group_id][self_qq]['lose_times']
    reply = "你今日决斗的战绩为：{}胜，{}负~".format(win_times, lose_times)
    return reply


def duel_rank(self, group_id):
    record_list = []

    for qq in self.duel_dict[group_id]:
        if done_today(self.duel_dict[group_id][qq]['date']) and \
                self.duel_dict[group_id][qq]['win_times'] >= self.duel_dict[group_id][qq]['lose_times']:
            record_list.append((qq,
                                self.duel_dict[group_id][qq]['win_times'] * 2 - self.duel_dict[group_id][qq][
                                    'lose_times']))
    if len(record_list) == 0:
        reply = "今天还没有人决斗过哦，过来试试吧~"
    else:
        record_list.sort(key=lambda k: k[1], reverse=True)
        reply = "下面是今日的决斗榜，今天你上榜了嘛~\n"
        for i in range(min(len(record_list), 5)):
            win_times = self.duel_dict[group_id][record_list[i][0]]['win_times']
            lose_times = self.duel_dict[group_id][record_list[i][0]]['lose_times']
            rate = win_times / (win_times + lose_times)
            reply += "{}.{} {}胜 胜率{}%\n" \
                .format(str(i + 1), record_list[i][0], win_times, round(rate * 100, 2))
        reply = reply.strip()
    return reply


async def duel_qq(self, bot, group_id, self_qq, opponent_qq):
    if self_qq == opponent_qq:
        reply = "你想自残吗……"
    else:
        try:
            self_info = await bot.get_group_member_info(group_id=int(group_id), user_id=int(self_qq))
            opponent_info = await bot.get_group_member_info(group_id=int(group_id), user_id=int(opponent_qq))
            if self_qq == PARTNER_QQ_NUMBER and opponent_qq == SELF_QQ_NUMBER:
                reply = "不急，等晚上再一起玩~"
            elif self_info['role'] == 'admin' or self_info['role'] == 'owner':
                if opponent_info['role'] == "admin" or opponent_info['role'] == "owner":
                    reply = "管理员之间的争斗，我管不了……"
                else:
                    await bot.set_group_ban(group_id=int(group_id), user_id=int(opponent_qq),
                                            duration=10 * 60)
                    reply = "一股强大的力量袭来……"
            elif opponent_info['role'] == "owner":
                await bot.set_group_ban(group_id=int(group_id), user_id=int(self_qq), duration=5 * 60)
                reply = "竟敢挑战群主，你将受到天罚！"
            elif str(opponent_info['user_id']) == SELF_QQ_NUMBER:
                await bot.set_group_ban(group_id=int(group_id), user_id=int(self_qq), duration=5 * 60)
                reply = "我定的规则，你觉得我会输吗~"
            elif opponent_info['role'] == "admin":
                await bot.set_group_ban(group_id=int(group_id), user_id=int(self_qq), duration=5 * 60)
                reply = "竟敢挑战管理员，你将受到天罚！"
            else:
                self_name = get_name(self_info)
                opponent_name = get_name(opponent_info)
                self_point = random.randint(1, 99)
                opponent_point = random.randint(1, 99)
                reply = "{}掷出了{}点\n{}掷出了{}点\n" \
                    .format(self_name, str(self_point), opponent_name, str(opponent_point))
                if self_point < opponent_point:
                    reply += "你在决斗中失败了……"
                    if self.duel_dict[group_id][self_qq]['multi_kill'] in multi_kill:
                        ban_time = (self.duel_dict[group_id][self_qq]['multi_kill'] - 3) * 5 + 10
                    else:
                        ban_time = 10
                    await bot.set_group_ban(group_id=int(group_id), user_id=int(self_qq), duration=ban_time * 60)

                    if self.duel_dict[group_id][self_qq]['multi_kill'] in multi_kill:
                        reply += "\n{}被终结了！".format(self_name)

                    record_duel_info(self.duel_dict[group_id], self_qq, False)
                    record_duel_info(self.duel_dict[group_id], opponent_qq, True)
                    update_dict(DUEL_PATH, self.duel_dict)
                    if self.duel_dict[group_id][opponent_qq]['multi_kill'] in multi_kill:
                        reply += "\n{}{}".format(opponent_name,
                                                 multi_kill[self.duel_dict[group_id][opponent_qq]['multi_kill']])

                elif self_point > opponent_point:
                    reply += "你在决斗中胜利了！"
                    if self.duel_dict[group_id][opponent_qq]['multi_kill'] in multi_kill:
                        ban_time = (self.duel_dict[group_id][opponent_qq]['multi_kill'] - 3) * 5 + 10
                    else:
                        ban_time = 10
                    await bot.set_group_ban(group_id=int(group_id), user_id=int(opponent_qq),
                                            duration=ban_time * 60)

                    if self.duel_dict[group_id][opponent_qq]['multi_kill'] in multi_kill:
                        reply += "\n{}被终结了！".format(opponent_name)

                    record_duel_info(self.duel_dict[group_id], self_qq, True)
                    record_duel_info(self.duel_dict[group_id], opponent_qq, False)
                    update_dict(DUEL_PATH, self.duel_dict)
                    if self.duel_dict[group_id][self_qq]['multi_kill'] in multi_kill:
                        reply += "\n{}{}".format(self_name,
                                                 multi_kill[self.duel_dict[group_id][self_qq]['multi_kill']])

                else:
                    reply += "平局！"
        except:
            reply = "群里貌似并没有这个人……"
    return reply