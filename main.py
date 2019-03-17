import re
from aiocqhttp import CQHttp
from mcstatus import MinecraftServer
from mcrcon import MCRcon

from crawler import *
from const import *

HOST = "172.17.67.53"  # '192.168.1.3' '172.17.67.53'
PORT = 8080
QQ_number = "2511310647"
partner_QQ_number = "424506920"
server_host = "wt.D.mcmiao.com"
server_port = "34874"
rcon_port = "34884"

debug = False

bot = CQHttp(api_root='http://127.0.0.1:5700/')


def load_player_qq():
    with open(player_qq_path, 'r') as f:
        player_infos = f.read().splitlines()

    player_qq_dict = {}

    for player_info in player_infos:
        info = player_info.split(" ")
        player_qq_dict[info[0]] = info[1]

    return player_qq_dict


player_qq_dict = load_player_qq()


def regex_match(pattern, message):
    if re.match(pattern, message, flags=0) is not None:
        return True
    return False


@bot.on_message('private')
async def handle_private_msg(content):
    if debug:
        print(content)

    message = ""
    if content['message'] == "你好":
        message = "你好呀~"

    elif content['message'] == "白名单":
        message = "申请白名单格式：\"白名单 游戏名\"\n" \
                  "其中，游戏名只能包含英文、数字、和下划线，不能有中文和横线"

    elif regex_match("^白名单 ", content['message']):
        if regex_match("^白名单 [a-zA-Z0-9_]{3,}$", content['message']):
            qq_number = str(content['sender']['user_id'])
            if qq_number in player_qq_dict:
                message = "你是" + player_qq_dict[qq_number] + "，你已经申请过白名单了，别想骗我！"
            else:
                player_name = re.match("^白名单 ([a-zA-Z0-9_]{3,})$", content['message'], flags=0).group(1)
                with open("data/rcon_password.txt", "r") as f:
                    rcon_password = f.readline()
                with MCRcon(host=server_host, password=rcon_password, port=int(rcon_port)) as mcr:
                    mcr.command("whitelist add " + player_name)
                player_qq_dict[qq_number] = player_name
                with open(player_qq_path, 'w+') as f:
                    for qq in player_qq_dict:
                        f.write(qq + " " + player_qq_dict[qq] + "\n")
                message = "白名单添加成功！"
        else:
            message = "游戏名格式有误！"

    elif regex_match("^我是谁", content['message']):
        qq_number = str(content['sender']['user_id'])
        if qq_number in player_qq_dict:
            message = "你是" + player_qq_dict[qq_number] + "！"
        else:
            message = "你都没有白名单，我哪知道。。。"

    if message is not "":
        await bot.send(content, message=message, at_sender=False, auto_escape=True)


@bot.on_message('group')
async def handle_group_msg(content):
    if debug:
        print(content)

    message = ""
    if content['group_id'] == 298466962:  # 影之乡服务器
        if content['message'] == "小紫" or content['message'] == "[CQ:at,qq=" + QQ_number + "] ":
            message = "你好呀，我是腐竹的搭档小紫。\n" \
                      "目前我可以:\n" \
                      "1. 添加白名单。（私聊我\"白名单\"获取详情）\n" \
                      "2. 获取服务器在线人数。（@我并发送在线人数）\n" \
                      "我刚从微信过来，目前蜗居在阿里云，还在成长中~"

        elif regex_match("^\\[CQ:at,qq=" + QQ_number + "\\] .*", content['message']):
            at_content = re.match("^\\[CQ:at,qq=" + QQ_number + "\\] (.*)", content['message'], flags=0).group(1)
            if debug:
                print(at_content)
            if at_content == "我爱你":
                if str(content['sender']['user_id']) == partner_QQ_number:
                    message = "我也爱你呀~"
                else:
                    message = "我不是那么随便的人~"
            elif at_content == "在线人数":
                server = MinecraftServer.lookup(server_host + ":" + server_port)
                players = server.status().players
                message = "在线人数：" + str(players.online) + "/" + str(players.max) + "\n"
            elif at_content == "服务器延迟":
                server = MinecraftServer.lookup(server_host + ":" + server_port)
                message = "服务器延迟：" + str(server.ping()) + "ms"

    if message is not "":
        await bot.send(content, message=message, at_sender=False, auto_escape=True)


@bot.on_notice('group_increase')
async def handle_group_increase(content):
    message = "新人你好，我是腐竹的搭档小紫，欢迎加入影之乡服务器！客户端在群共享中，想要获取白名单请私聊我\"白名单\"，其他事宜请阅读群公告。"
    await bot.send(content, message=message, at_sender=True, auto_escape=True)


@bot.on_request('group')
async def handle_group_request(content):
    if content['group_id'] == 298466962:
        if content['comment'] == "mcbbs" or content['comment'] == "贴吧" or content['comment'] == "论坛":
            return {'approve': True}


bot.run(host=HOST, port=PORT)