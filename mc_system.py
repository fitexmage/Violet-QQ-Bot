from config import *
from util import *

from mcstatus import MinecraftServer
from mcrcon import MCRcon


class MC_System:
    def __init__(self):
        self.player_qq_dict = load_player_qq()

        with open(rcon_password_path, "r") as f:
            self.rcon_password = f.readline()

    def update_qq_dict(self):
        with open(player_qq_path, 'w+') as f:
            for qq in self.player_qq_dict:
                f.write(qq + " " + self.player_qq_dict[qq] + "\n")

    def rcon_command(self, command):
        with MCRcon(host=server_host, password=self.rcon_password, port=rcon_port) as mcr:
            text = mcr.command(command)
            text = re.sub('§.', "", text).strip()
            return text

    def reply_intro(self):
        reply = "你好呀~我是腐竹的人工智能搭档小紫，目前我可以:\n" \
                "1. 添加白名单。（私聊我\"白名单\"获取详情）\n" \
                "2. 获取自己的游戏名。（@我并发送\"我是谁\"）\n" \
                "3. 获取其他玩家的游戏名。（@我并发送\"xxxxxx（QQ号）是谁\"）\n" \
                "3. 获取服务器在线人数或不在线人数。（@我并发送\"在线人数\"或\"不在线人数\"）\n" \
                "4. 获取服务器延迟。（@我并发送\"服务器延迟\"）"
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
                    self.update_qq_dict()
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

    def reply_group_msg(self, context, at_content):
        qq_number = str(context['sender']['user_id'])

        reply = ""

        if regex_match("我是谁", at_content):
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
            server = MinecraftServer.lookup(server_host + ":" + str(server_port))
            reply = "服务器延迟：" + str(server.ping()) + "ms"
        elif regex_match('^mc指令/.*', at_content):
            if qq_number == partner_QQ_number:
                command = at_content.replace("/", "")
                reply = self.rcon_command(command)
            else:
                reply = "这个指令只有我和腐竹可以用！"

        # else:
        # url = search_url(at_content)
        # if url:
        #     if self.debug:
        #         print("URL: " + url)
        #     reply = crawler_result(url)
        # if reply is None:
        #     reply = "对不起，我不太懂，我还需要学习~"

        return reply