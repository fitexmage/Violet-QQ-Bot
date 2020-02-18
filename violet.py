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

    def reply_group_msg(self, bot, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = None

        if random.random() < 0.05:
            reply = random.choice(["是的呀", "我也觉得是~", "没错", "哈哈哈"])

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
            reply = "现在的时间是：{}".format(str(time_now()).split('.')[0])
        elif re.match('你在哪', at_content):
            print(self.cur_lat, self.cur_lon)
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
            if len(par_list) == 1:
                reply = "请选择一位对手吧！"
            else:
                self_qq = str(context['user_id'])
                opponent_qq = par_list[1]

                info = await bot.get_group_member_info(group_id=context['group_id'], user_id=int(opponent_qq))
                print(info)


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
