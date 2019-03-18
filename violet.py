from util import *

from mcstatus import MinecraftServer
from mcrcon import MCRcon

class Violet:
    def __init__(self):
        self.enable = True
        self.player_qq_dict = load_player_qq()

    def reply_private_msg(self, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = ""

        if message == "你好":
            reply = "你好呀~"

        elif message == "白名单":
            reply = "申请白名单格式：白名单 游戏名\n" \
                      "如：白名单 Fitexmage\n" \
                      "注意：游戏名只能包含英文、数字、和下划线，不能有中文和横线"

        elif regex_match("^白名单 ", message):
            if regex_match("^白名单 [a-zA-Z0-9_]{3,}$", message):
                if qq_number in self.player_qq_dict:
                    reply = "你是" + self.player_qq_dict[qq_number] + "，你已经申请过白名单了，别想骗我！"
                else:
                    player_name = re.match("^白名单 ([a-zA-Z0-9_]{3,})$", message, flags=0).group(1)
                    with open(rcon_password_path, "r") as f:
                        rcon_password = f.readline()
                    with MCRcon(host=server_host, password=rcon_password, port=rcon_port) as mcr:
                        mcr.command("whitelist add " + player_name)
                    self.player_qq_dict[qq_number] = player_name
                    with open(player_qq_path, 'w+') as f:
                        for qq in self.player_qq_dict:
                            f.write(qq + " " + self.player_qq_dict[qq] + "\n")
                    reply = "白名单添加成功！"
            else:
                reply = "游戏名格式有误！"

        elif regex_match("^我是谁", message):
            if qq_number in self.player_qq_dict:
                reply = "你是" + self.player_qq_dict[qq_number] + "！"
            else:
                reply = "你都没有白名单，我哪知道。。。"

        return reply

    def reply_group_msg(self, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = ""

        if message == "小紫 启" and qq_number == partner_QQ_number:
            reply = self.start()
        elif message == "小紫 散" and qq_number == partner_QQ_number:
            reply = self.close()

        elif self.enable:
            if context['group_id'] == 298466962:  # 影之乡服务器
                if message == "小紫" or message == "[CQ:at,qq=" + QQ_number + "] ":
                    reply = "你好呀，我是腐竹的搭档小紫。\n" \
                              "目前我可以:\n" \
                              "1. 添加白名单。（私聊我\"白名单\"获取详情）\n" \
                              "2. 获取服务器在线人数。（@我并发送在线人数）\n" \
                              "我刚从微信过来，目前蜗居在阿里云，还在成长中~"

                elif regex_match("^\\[CQ:at,qq=" + QQ_number + "\\] .*", message):
                    at_content = re.match("^\\[CQ:at,qq=" + QQ_number + "\\] (.*)", message, flags=0).group(1)
                    if debug:
                        print(at_content)

                    if at_content == "我爱你":
                        if qq_number == partner_QQ_number:
                            reply = "我也爱你呀~"
                        else:
                            reply = "我不是那么随便的人~"
                    elif at_content == "在线人数":
                        server = MinecraftServer.lookup(server_host + ":" + str(server_port))
                        players = server.status().players
                        reply = "在线人数：" + str(players.online) + "/" + str(players.max)
                    elif at_content == "服务器延迟":
                        server = MinecraftServer.lookup(server_host + ":" + str(server_port))
                        reply = "服务器延迟：" + str(server.ping()) + "ms"

        return reply

    def start(self):
        self.enable = True
        reply = "小紫已启动"
        return reply

    def close(self):
        self.enable = False
        reply = "小紫已关闭"
        return reply