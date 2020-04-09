from util import *
from config import *

from mcstatus import MinecraftServer
from mcrcon import MCRcon


def rcon_command(self, command):
    with MCRcon(host=SERVER_HOST, password=self.rcon_password, port=RCON_PORT) as mcr:
        text = mcr.command(command)
        text = re.sub('§.', "", text).strip()
        return text


def intro():
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


def add_white_list(self, message, qq_number):
    if regex_match("白名单 [a-zA-Z0-9_?]{3,20}$", message):
        if qq_number in self.player_qq_dict:
            reply = "你是" + self.player_qq_dict[qq_number] + "，你已经申请过白名单了，别想骗我！"
        else:
            player_name = re.match("白名单 ([a-zA-Z0-9_?]{3})$", message).group(1)
            rcon_command(self, "wladd " + player_name)
            self.player_qq_dict[qq_number] = player_name
            update_file(PLAYER_QQ_PATH, self.player_qq_dict)
            reply = "白名单添加成功！"
    else:
        reply = "游戏名格式有误！"
    return reply


def white_list_intro():
    reply = "申请白名单格式：白名单 游戏名\n" \
            "如：白名单 Fitexmage\n" \
            "注意：游戏名只能包含英文、数字、和下划线，不能有中文和横线"
    return reply


def who_am_i(self, qq_number):
    if qq_number in self.player_qq_dict:
        reply = "你是" + self.player_qq_dict[qq_number] + "！"
    else:
        reply = "你都没有白名单，我哪知道。。。"
    return reply


def who_is_qq(self, message):
    qq_number = re.search("[0-9]+", message).group(0)
    if qq_number in self.player_qq_dict:
        reply = "这位玩家是" + self.player_qq_dict[qq_number] + "！"
    else:
        reply = "此人未获得白名单！"
    return reply


def who_is_name(self, at_content):
    reply = ""
    id = re.search("(.+)是谁", at_content).group(1)
    for qq_number in self.player_qq_dict:
        if self.player_qq_dict[qq_number] == id:
            reply = "这位玩家的QQ是" + qq_number + "！"
            break
    if reply == "":
        reply = "此人未获得白名单！"
    return reply


def offline(self):
    num_online = int(re.search('[0-9]+', rcon_command(self, "list")).group())
    num_player = len(self.player_qq_dict)
    num_offline = num_player - num_online
    reply = "当前有" + str(num_offline) + "个玩家不在线，最大不在线人数为" + str(num_player) + "个玩家."
    return reply


def server_ping():
    server = MinecraftServer.lookup(SERVER_HOST + ":" + str(SERVER_PORT))
    reply = "服务器延迟：" + str(server.ping()) + "ms"
    return reply