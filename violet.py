from util import *
from crawler import *
from mc_system import MC_System
from ff_system import FF_System

class Violet:
    def __init__(self):
        self.enable = True
        self.debug = False

        self.mc_system = MC_System()
        self.ff_ststem = FF_System()

    def reply_intro(self):
        reply = "你好呀~我是腐竹的人工智能搭档小紫，目前我的辅助范围有:\n" \
                "1. MC影之乡服务器。（@我并发送\"MC\"或\"影之乡\"获取详情）\n" \
                "2. 最终幻想14。（@我并发送\"最终幻想14\"或\"ff14\"获取详情）"
        return reply

    def reply_private_msg(self, context):
        message = context['message']

        reply = None

        if self.enable:
            if message == "你好":
                reply = "你好呀~"

            if reply is not None:
                reply = self.mc_system.reply_private_msg(context)

            if reply is not None:
                reply = self.ff_ststem.reply_private_msg(context)

        return reply

    def reply_group_msg(self, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = None

        if message == "小紫 启" or message == "启" and qq_number == partner_QQ_number:
            reply = self.start()
        elif message == "小紫 散" or message == "散" and qq_number == partner_QQ_number:
            reply = self.close()

        elif self.enable:
            if message == "小紫" or message == "@【影之接待】小紫" or message == "[CQ:at,qq=" + self_QQ_number + "] ":
                reply = self.reply_intro()
            elif message in {"mc", "MC", "影之乡", "硬纸箱"}:
                reply = self.mc_system.reply_intro()
            elif message in {"最终幻想14", "ff14"}:
                reply = self.ff_ststem.reply_intro()

            elif regex_match("\\[CQ:at,qq=" + self_QQ_number + "\\].*", message):
                at_content = re.match("^\\[CQ:at,qq=" + self_QQ_number + "\\](.*)", message).group(1).strip()
                print(at_content)
                if self.debug:
                    print("Context: " + at_content)
                if regex_match("你是谁", at_content):
                    reply = "我是小紫呀~"
                elif at_content == "我爱你":
                    if qq_number == partner_QQ_number:
                        reply = "我也爱你呀~"
                    else:
                        reply = "我不是那么随便的人~"
                elif at_content == "debug":
                    if qq_number == partner_QQ_number:
                        self.debug = not self.debug
                        reply = "Debug模式已更换为：" + str(self.debug) + "!"

                print(reply)
                if reply is None:
                    print("mc")
                    reply = self.mc_system.reply_group_msg(context, at_content)
                print(reply)
                if reply is None:
                    print("ff")
                    reply = self.ff_ststem.reply_group_msg(context, at_content)

        return reply

    def start(self):
        self.enable = True
        reply = "小紫已启动"
        return reply

    def close(self):
        self.enable = False
        reply = "小紫已关闭"
        return reply
