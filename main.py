from config import *
from violet import Violet

from aiocqhttp import CQHttp
import re

bot = CQHttp(api_root='http://127.0.0.1:5700/')
violet = Violet()


@bot.on_message('private')
async def handle_private_msg(context):
    if violet.debug:
        print(context)

    if context['group_id'] == int(SHADOWVILLAGE_QQ_NUMBER):
        reply = violet.reply_private_msg(context)
        if reply is not None:
            if isinstance(reply, list):
                for r in reply:
                    await bot.send(context, message=r, at_sender=False, auto_escape=True)
            else:
                await bot.send(context, message=reply, at_sender=False, auto_escape=True)


@bot.on_message('group')
async def handle_group_msg(context):
    if violet.debug:
        print(context)

    reply = await violet.reply_group_msg(bot, context)
    if reply is not None:
        if isinstance(reply, list):
            for r in reply:
                await bot.send(context, message=r, at_sender=False, auto_escape=False)
        else:
            await bot.send(context, message=reply, at_sender=False, auto_escape=False)


@bot.on_notice('group_increase')
async def handle_group_increase(context):
    if violet.debug:
        print(context)

    if violet.enable and context['group_id'] == int(SHADOWVILLAGE_QQ_NUMBER):
        reply = "新人你好，我是人工智能小紫，欢迎加入影之乡服务器！\n现在为服务器大维护阶段，可从群文件下载番外周目进行体验，其他事宜请阅读群公告。"
        # reply = "新人你好，我是人工智能小紫，欢迎加入影之乡服务器！\n请在群共享中下载客户端，想要获取白名单请私聊我\"白名单\"，其他事宜请阅读群公告。"
        await bot.send(context, message=reply, at_sender=True, auto_escape=True)


@bot.on_notice('group_decrease')
async def handle_group_decrease(context):
    if violet.debug:
        print(context)

    if context['group_id'] == int(SHADOWVILLAGE_QQ_NUMBER):
        qq_number = str(context['user_id'])
        if qq_number in violet.mc_system.player_qq_dict:
            violet.mc_system.rcon_command("wldel " + violet.mc_system.player_qq_dict[qq_number])
            violet.mc_system.player_qq_dict.pop(qq_number)
            violet.mc_system.update_qq_dict()


@bot.on_request('group')
async def handle_group_request(context):
    if violet.debug:
        print(context)

    if violet.enable:
        if context['group_id'] == int(SHADOWVILLAGE_QQ_NUMBER):
            comment = "问题：从哪里知道的影之乡？\n答案："
            answer = re.match(comment + "(.*)", context['comment']).group(1).lower()

            if re.search("bbs", answer) or \
                    re.search("论坛", answer) or \
                    re.search("贴吧", answer) or \
                    re.search("b站", answer):
                return {'approve': True}


bot.run(host=HOST, port=PORT)
