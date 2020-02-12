from config import *
from util import *
from crawler import get_combat_data

class FF_System:
    def __init__(self):
        print()

    def reply_intro(self):
        reply = "你好呀~我是腐竹的人工智能搭档小紫，目前我可以:\n" \
                "1. 我也不知道我能干啥，正在跟隔壁獭獭学习\n"
        return reply

    def reply_private_msg(self, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = None

        return reply

    def reply_group_msg(self, context, at_content):
        qq_number = str(context['sender']['user_id'])

        reply = None

        if regex_match('^ff指令/.*', at_content):
            command = at_content.replace("ff指令/", "")
            reply = get_combat_data(command)

        return reply
