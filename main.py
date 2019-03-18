from const import *
from violet import *

from aiocqhttp import CQHttp

bot = CQHttp(api_root='http://127.0.0.1:5700/')
violet = Violet()

@bot.on_message('private')
async def handle_private_msg(context):
    if debug:
        print(context)

    message = violet.reply_private_msg(context)
    if message is not "":
        await bot.send(context, message=message, at_sender=False, auto_escape=True)


@bot.on_message('group')
async def handle_group_msg(context):
    if debug:
        print(context)

    message = violet.reply_group_msg(context)
    if message is not "":
        await bot.send(context, message=message, at_sender=False, auto_escape=True)


@bot.on_notice('group_increase')
async def handle_group_increase(content):
    if violet.enable:
        message = "新人你好，我是腐竹的搭档小紫，欢迎加入影之乡服务器！客户端在群共享中，想要获取白名单请私聊我\"白名单\"，其他事宜请阅读群公告。"
        await bot.send(content, message=message, at_sender=True, auto_escape=True)


@bot.on_request('group')
async def handle_group_request(content):
    if violet.enable:
        if content['group_id'] == 298466962:
            if content['comment'] == "mcbbs" or content['comment'] == "贴吧" or content['comment'] == "论坛":
                return {'approve': True}


# bot.run(host=HOST, port=PORT)

print(auto_crawler("如何采矿"))