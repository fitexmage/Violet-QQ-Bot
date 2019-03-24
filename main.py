from const import *
from violet import Violet

from aiocqhttp import CQHttp

bot = CQHttp(api_root='http://127.0.0.1:5700/')
violet = Violet()


@bot.on_message('private')
async def handle_private_msg(context):
    if violet.debug:
        print(context)

    reply = violet.reply_private_msg(context)
    if reply is not "":
        await bot.send(context, message=reply, at_sender=False, auto_escape=True)


@bot.on_message('group')
async def handle_group_msg(context):
    if violet.debug:
        print(context)

    reply = violet.reply_group_msg(context)
    if reply is not "":
        await bot.send(context, message=reply, at_sender=False, auto_escape=True)


@bot.on_notice('group_increase')
async def handle_group_increase(context):
    if violet.debug:
        print(context)

    if violet.enable:
        reply = "新人你好，我是人工智能小紫，欢迎加入影之乡服务器！\n请在群共享中下载客户端，想要获取白名单请私聊我\"白名单\"，其他事宜请阅读群公告。"
        await bot.send(context, message=reply, at_sender=True, auto_escape=True)


@bot.on_request('group')
async def handle_group_request(context):
    print(context)

    if violet.enable:
        if context['group_id'] == 298466962:
            if context['comment'].lower() == "mcbbs" or context['comment'] == "贴吧" or context['comment'] == "论坛":
                return {'approve': True}


bot.run(host=HOST, port=PORT)
