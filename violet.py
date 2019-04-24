from util import *
from crawler import *

from mcstatus import MinecraftServer
from mcrcon import MCRcon


class Violet:
    def __init__(self):
        self.enable = True
        self.player_qq_dict = load_player_qq()
        self.syn_chat = True
        self.debug = False

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

            elif regex_match("白名单 ", message=message):
                if regex_match("白名单 [a-zA-Z0-9_]{3,}$", message):
                    if qq_number in self.player_qq_dict:
                        reply = "你是" + self.player_qq_dict[qq_number] + "，你已经申请过白名单了，别想骗我！"
                    else:
                        player_name = re.match("白名单 ([a-zA-Z0-9_]{3,})$", message).group(1)
                        self.rcon_command("whitelist add " + player_name)
                        self.player_qq_dict[qq_number] = player_name
                        self.update_qq_dict()
                        reply = "白名单添加成功！"
                else:
                    reply = "游戏名格式有误！"

            elif regex_match("我是谁", message):
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
                            "2. 获取自己的游戏名。（@我并发送\"我是谁\"）\n" \
                            "3. 获取其他玩家的游戏名。（@我并发送\"xxxxxx（QQ号）是谁\"）\n" \
                            "3. 获取服务器在线人数或不在线人数。（@我并发送\"在线人数\"或\"不在线人数\"）\n" \
                            "4. 获取服务器延迟。（@我并发送\"服务器延迟\"）\n" \
                            "5. 回答有关游戏的问题。（@我并发送任意问题）"

                elif regex_match("\\[CQ:at,qq=" + QQ_number + "\\].*", message):
                    at_content = re.match("^\\[CQ:at,qq=" + QQ_number + "\\](.*)", message).group(1).strip()
                    if self.debug:
                        print(at_content)

                    if regex_match("你是谁", at_content):
                        reply = "我是小紫呀~"
                    elif regex_match("我是谁", at_content):
                        if qq_number in self.player_qq_dict:
                            reply = "你是" + self.player_qq_dict[qq_number] + "！"
                        else:
                            reply = "你都没有白名单，我哪知道。。。"
                    elif regex_match("[0-9]+.*是谁", at_content):
                        qq_number = re.search("[0-9]+", at_content).group(0)
                        if qq_number in self.player_qq_dict:
                            reply = "这位玩家是" + self.player_qq_dict[qq_number] + "！"
                        else:
                            reply = "此人未获得白名单！"
                    elif at_content == "我爱你":
                        if qq_number == partner_QQ_number:
                            reply = "我也爱你呀~"
                        else:
                            reply = "我不是那么随便的人~"
                    elif regex_match('不在线', at_content):
                        num_online = int(re.search('[0-9]+', self.rcon_command("list")).group())
                        num_player = len(self.player_qq_dict)
                        num_offline = num_player - num_online
                        reply = "当前有" + str(num_offline) + "个玩家不在线，最大不在线人数为" + str(num_player) + "个玩家."
                    elif regex_match('在线', at_content):
                        reply = self.rcon_command("list")
                    elif at_content == "服务器延迟":
                        server = MinecraftServer.lookup(server_host + ":" + str(server_port))
                        reply = "服务器延迟：" + str(server.ping()) + "ms"
                    elif regex_match('/.*', at_content):
                        if qq_number == partner_QQ_number:
                            command = at_content.replace("/", "")
                            reply = self.rcon_command(command)
                    elif at_content == "切换聊天同步":
                        if qq_number == partner_QQ_number:
                            self.syn_chat = not self.syn_chat
                            reply = "聊天同步已切换为：" + str(self.syn_chat) + "!"
                    elif regex_match('(.+)(是什么|是啥|怎么用)', at_content):
                        question = re.match('(.+)(是什么|是啥|怎么用)', at_content).group(1)
                        reply = crawler_mcmod(question)
                        if reply is None:
                            reply = "对不起，我不太懂，我还需要学习~"
                    elif at_content == "debug":
                        if qq_number == partner_QQ_number:
                            self.debug = not self.debug
                            reply = "Debug模式已更换为：" + str(self.debug) + "!"
                    else:
                        url = search_url(at_content)
                        if url:
                            if self.debug:
                                print(url)
                            reply = crawler_result(url)
                        if reply is None:
                            reply = "对不起，我不太懂，我还需要学习~"
                else:
                    if self.syn_chat:
                        if qq_number in self.player_qq_dict:
                            message = re.sub('\[.*\]', "", message).strip()
                            if message is not "":
                                self.rcon_command(
                                    "svs synchat §2[群]§f<§2" + self.player_qq_dict[qq_number] + "§f> " + message)

        return reply

    def start(self):
        self.enable = True
        reply = "小紫已启动"
        return reply

    def close(self):
        self.enable = False
        reply = "小紫已关闭"
        return reply

regex = re.match('(.+)(是什么|是啥|怎么用)', "苹果是啥")
print(regex.group(2))