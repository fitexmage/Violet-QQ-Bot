from config import *
from util import *

from mcstatus import MinecraftServer
from mcrcon import MCRcon

import datetime


class MC_System:
    def __init__(self):
        self.player_qq_dict = load_dict(PLAYER_QQ_PATH)
        self.luck_dict = load_dict(MC_LUCK_PATH)

        with open(RCON_PASSWORD_PATH, "r") as f:
            self.rcon_password = f.readline()

    def rcon_command(self, command):
        with MCRcon(host=SERVER_HOST, password=self.rcon_password, port=RCON_PORT) as mcr:
            text = mcr.command(command)
            text = re.sub('§.', "", text).strip()
            return text

    def reply_intro(self):
        reply = "你好呀~我是腐竹的人工智能搭档小紫，目前我可以:\n" \
                "*私聊我：\n" \
                "1. 白名单：添加白名单。\n" \
                "在群里@我并发送：\n" \
                "1. 我是谁：获取自己的游戏名。\n" \
                "2. xxxxxx（QQ号）是谁：获取其他玩家的游戏名。\n" \
                "3. 在线人数或不在线人数：获取服务器在线人数或不在线人数。\n" \
                "4. 延迟：获取服务器延迟。\n\n" \
                "*在群里直接发送：\n" \
                "1. /mc 占卜：让小紫为你占卜今日的mc游戏运势。"
        return reply

    def reply_private_msg(self, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = None

        if regex_match("白名单 ", message):
            if regex_match("白名单 [a-zA-Z0-9_?]{3,}$", message):
                if qq_number in self.player_qq_dict:
                    reply = "你是" + self.player_qq_dict[qq_number] + "，你已经申请过白名单了，别想骗我！"
                else:
                    player_name = re.match("白名单 ([a-zA-Z0-9_?]{3,})$", message).group(1)
                    self.rcon_command("wladd " + player_name)
                    self.player_qq_dict[qq_number] = player_name
                    update_dict(PLAYER_QQ_PATH, self.player_qq_dict)
                    reply = "白名单添加成功！"
            else:
                reply = "游戏名格式有误！"

        elif "白名单" in message:
            reply = "申请白名单格式：白名单 游戏名\n" \
                    "如：白名单 Fitexmage\n" \
                    "注意：游戏名只能包含英文、数字、和下划线，不能有中文和横线"

        elif regex_match("我是谁", message):
            if qq_number in self.player_qq_dict:
                reply = "你是" + self.player_qq_dict[qq_number] + "！"
            else:
                reply = "你都没有白名单，我哪知道。。。"

        elif regex_match(".*[0-9]+.*是谁", message):
            qq_number = re.search("[0-9]+", message).group(0)
            if qq_number in self.player_qq_dict:
                reply = "这位玩家是" + self.player_qq_dict[qq_number] + "！"
            else:
                reply = "此人未获得白名单！"
        return reply

    def reply_group_at_msg(self, context, at_content):
        qq_number = str(context['sender']['user_id'])

        reply = None

        if at_content in {"mc", "MC", "影之乡", "硬纸箱"}:
            reply = self.reply_intro()
        elif regex_match("我是谁", at_content):
            if qq_number in self.player_qq_dict:
                reply = "你是" + self.player_qq_dict[qq_number] + "！"
            else:
                reply = "你都没有白名单，我哪知道。。。"
        elif regex_match("[0-9]+.*是谁.*", at_content):
            qq_number = re.search("[0-9]+", at_content).group(0)
            if qq_number in self.player_qq_dict:
                reply = "这位玩家是" + self.player_qq_dict[qq_number] + "！"
            else:
                reply = "此人未获得白名单！"
        elif regex_match(".*是谁.*", at_content):
            id = re.search("(.*)是谁", at_content).group(1)
            get_result = False
            for qq_number in self.player_qq_dict:
                if self.player_qq_dict[qq_number] == id:
                    reply = "这位玩家的QQ是" + qq_number + "！"
                    get_result = True
                    break
            if not get_result:
                reply = "此人未获得白名单！"

        elif regex_match('在线', at_content):
            reply = self.rcon_command("list")
        elif regex_match('不在线', at_content):
            num_online = int(re.search('[0-9]+', self.rcon_command("list")).group())
            num_player = len(self.player_qq_dict)
            num_offline = num_player - num_online
            reply = "当前有" + str(num_offline) + "个玩家不在线，最大不在线人数为" + str(num_player) + "个玩家."
        elif at_content == "服务器延迟":
            server = MinecraftServer.lookup(SERVER_HOST + ":" + str(SERVER_PORT))
            reply = "服务器延迟：" + str(server.ping()) + "ms"

        return reply

    def reply_group_cmd_msg(self, context, command):
        qq_number = str(context['sender']['user_id'])

        if command == 'help':
            reply = self.reply_intro()
        # elif command == '占卜':
        #     date = str(datetime.date.today())
        #     if qq_number not in self.luck_dict or self.luck_dict[qq_number] != date:
        #         reply = "下面是小紫采用人工智能秘术所做出的占卜：\n" \
        #                 "1. 战斗运势：\n" \
        #                 "打怪：" + luck_parser(get_gaussian(), dungeon_luck) + "\n" \
        #                 "打BOSS：" + luck_parser(get_gaussian(), boss_luck) + "\n\n" \
        #                 "挖矿：" + luck_parser(get_gaussian(), treature_luck) + "\n" \
        #                 "制作：" + luck_parser(get_gaussian(), treature_luck) + "\n" \
        #                 "交友：" + luck_parser(get_gaussian(), friend_luck) + "\n" \
        #                 "财产安全：" + luck_parser(get_gaussian(), friend_luck) + "\n" \
        #                 "建筑：" + luck_parser(get_gaussian(), decorate_luck)
        #         self.luck_dict[qq_number] = date
        #         update_dict(ff_luck_path, self.luck_dict)
        #     else:
        #         reply = "你今天已经占卜过啦，请明天再来！"
        elif qq_number == PARTNER_QQ_NUMBER:
            reply = self.rcon_command(command)
        else:
            reply = "这个指令只有我和腐竹可以用！"

        return reply