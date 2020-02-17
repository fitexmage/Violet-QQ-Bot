from util import *
from crawler import *
from mc_system import MC_System
from ff_system import FF_System

import os

class Violet:
    def __init__(self):
        self.enable = True
        self.debug = False

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

    def reply_group_msg(self, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = None

        if qq_number == PARTNER_QQ_NUMBER:
            if message == "小紫 启":
                reply = self.start()
            elif message == "小紫 散":
                reply = self.close()

        if self.enable:
            if message == "小紫" or message == "@【影之接待】小紫" or message == "[CQ:at,qq=" + SELF_QQ_NUMBER + "] ":
                reply = self.reply_intro()

            elif regex_match('\\[CQ:at,qq={}\\].*'.format(SELF_QQ_NUMBER), message):
                at_content = re.match('\\[CQ:at,qq={}\\].*'.format(SELF_QQ_NUMBER), message).group(1).strip()
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
                elif at_content == "debug":
                    if qq_number == PARTNER_QQ_NUMBER:
                        self.debug = not self.debug
                        reply = "Debug模式已更换为：{}！".format(str(self.debug))

                if reply is None:
                    reply = self.mc_system.reply_group_at_msg(context, at_content)
                if reply is None:
                    reply = self.ff_ststem.reply_group_at_msg(context, at_content)

            elif regex_match('^/mc .+', message):
                command = re.match('^/mc (.+)', message).group(1)
                reply = self.mc_system.reply_group_cmd_msg(context, command)

            elif regex_match('^/ff .+', message):
                command = re.match('^/ff (.+)', message).group(1)
                reply = self.ff_ststem.reply_group_cmd_msg(context, command)
        return reply

    def start(self):
        self.enable = True
        reply = "小紫已启动"
        return reply

    def close(self):
        self.enable = False
        reply = "小紫已关闭"
        return reply