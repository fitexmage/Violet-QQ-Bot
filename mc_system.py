from mc_util import *
from config import *
from util import *


class MC_System:
    def __init__(self):
        self.player_qq_dict = load_file(PLAYER_QQ_PATH)
        self.luck_dict = load_file(MC_LUCK_PATH)

    def reply_private_msg(self, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = None

        if regex_match("白名单 .+", message):
            reply = add_white_list(self, message, qq_number)
        elif "白名单" in message:
            reply = white_list_intro()
        elif regex_match("我是谁", message):
            reply = who_am_i(self, qq_number)
        elif regex_match(".*[0-9]+.*是谁", message):
            reply = who_is_qq(self, message)
        return reply

    def reply_group_at_msg(self, context, at_content):
        qq_number = str(context['sender']['user_id'])

        reply = None

        if at_content in {"mc", "MC", "影之乡", "硬纸箱"}:
            reply = intro()
        elif regex_match("我是谁", at_content):
            reply = who_am_i(self, qq_number)
        elif regex_match("[0-9]+.*是谁.*", at_content):
            reply = who_is_qq(self, at_content)
        elif regex_match(".*是谁.*", at_content):
            reply = who_is_name(self, at_content)
        elif regex_match('在线', at_content):
            reply = rcon_command(self, "list")
        elif regex_match('不在线', at_content):
            reply = offline(self)
        elif at_content == "服务器延迟":
            reply = server_ping()

        return reply

    def reply_group_cmd_msg(self, context, par_list):
        qq_number = context['sender']['user_id']

        if par_list[0] == 'help':
            reply = intro()
        # elif command == '占卜':
        #     if not done_today(self.luck_dict, qq_number):
        elif qq_number == PARTNER_QQ:
            reply = rcon_command(self, ' '.join(par_list))
        else:
            reply = "这个指令只有我和腐竹可以用！"

        return reply