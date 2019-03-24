from util import *
from crawler import *

from mcstatus import MinecraftServer
from mcrcon import MCRcon


class Violet:
    def __init__(self):
        self.enable = True
        self.player_qq_dict = load_player_qq()
        self.debug = False

        with open(rcon_password_path, "r") as f:
            self.rcon_password = f.readline()

    def reply_private_msg(self, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = ""

        if self.enable:
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
                        player_name = re.match("^白名单 ([a-zA-Z0-9_]{3,})$", message).group(1)
                        with MCRcon(host=server_host, password=self.rcon_password, port=rcon_port) as mcr:
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
                    reply = "你好呀，我是腐竹的人工智能搭档小紫。\n" \
                            "目前我可以:\n" \
                            "1. 添加白名单。（私聊我\"白名单\"获取详情）\n" \
                            "2. 获取服务器在线人数。（@我并发送\"在线人数\"）\n" \
                            "3. 获取服务器延迟。（@我并发送\"服务器延迟\"）\n\n" \
                            "我刚从微信过来，还不太适应QQ，更多功能正在添加中~"

                elif regex_match("^\\[CQ:at,qq=" + QQ_number + "\\] .*", message):
                    at_content = re.match("^\\[CQ:at,qq=" + QQ_number + "\\] (.*)", message).group(1)
                    if self.debug:
                        print(at_content)

                    if at_content == "我爱你":
                        if qq_number == partner_QQ_number:
                            reply = "我也爱你呀~"
                        else:
                            reply = "我不是那么随便的人~"
                    elif at_content == "在线人数":
                        with MCRcon(host=server_host, password=self.rcon_password, port=rcon_port) as mcr:
                            text = mcr.command("list")
                            reply = re.sub('§.', "", text).strip()
                    elif at_content == "服务器延迟":
                        server = MinecraftServer.lookup(server_host + ":" + str(server_port))
                        reply = "服务器延迟：" + str(server.ping()) + "ms"
                    elif regex_match('^/.*', at_content):
                        if qq_number == partner_QQ_number:
                            with MCRcon(host=server_host, password=self.rcon_password, port=rcon_port) as mcr:
                                command = at_content.replace("/", "")
                                text = mcr.command(command)
                                reply = re.sub('§.', "", text).strip()
                    elif at_content == "debug":
                        if qq_number == partner_QQ_number:
                            self.debug = not self.debug
                            reply = "Debug模式已更换为：" + str(self.debug) + "!"
                    else:
                        url = search_url(at_content)
                        if url is not "":
                            if self.debug:
                                print(url)
                            reply = crawler_result(url)
                else:
                    if random.randint(0,1) == 0:
                        with MCRcon(host=server_host, password=self.rcon_password, port=rcon_port) as mcr:
                            mcr.command("say §f<§2" + context['sender']['card'] + "§f> " + message)

        return reply

    def start(self):
        self.enable = True
        reply = "小紫已启动"
        return reply

    def close(self):
        self.enable = False
        reply = "小紫已关闭"
        return reply