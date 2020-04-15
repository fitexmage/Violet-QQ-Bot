from violet_util import *
from util import *
from mc_system import MC_System
from ff_system import FF_System
from crawler import crawl_zhidao


class Violet:
    def __init__(self):
        self.enable = True
        self.debug = False
        self.cur_lat = random.uniform(-90, 90)
        self.cur_lon = random.uniform(-180, 180)
        self.last_reply = None

        self.duel_dict = load_file(DUEL_PATH)

        self.mc_system = MC_System()
        self.ff_ststem = FF_System()

    def reply_private_msg(self, context):
        message = context['message']

        reply = None

        if self.enable:
            if message == "你好":
                reply = "你好呀~"
            else:
                reply = "目前私聊业务不开放，请转至群聊！"

            # if reply is None:
            #     reply = self.mc_system.reply_private_msg(context)
            #
            # if reply is None:
            #     reply = self.ff_ststem.reply_private_msg(context)

        return reply

    async def reply_group_msg(self, bot, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = None

        if qq_number == PARTNER_QQ:
            if message == "小紫 启":
                reply = self.start()
            elif message == "小紫 散":
                reply = self.close()

        if self.enable:
            if message == "[CQ:at,qq=" + SELF_QQ + "] ":
                reply = intro()
            elif regex_match('\\[CQ:at,qq={}\\].*'.format(SELF_QQ), message):
                reply = self.reply_group_at_msg(context, message, qq_number)
            elif regex_match('^/', message):
                reply = await self.reply_group_cmd_msg(bot, context, message)
            else:
                group_id = str(context['group_id'])
                save_message(group_id, qq_number, message)

                if random.random() < 0.09 and group_id == SHADOWVILLAGE_QQ and '[CQ:' not in message:
                    reply = crawl_zhidao(message)

        return reply

    def reply_group_at_msg(self, context, message, qq_number):
        at_content = re.sub('\\[CQ:at,qq=[0-9]+\\] ', '', message)

        reply = None

        if self.debug:
            print("Context: " + at_content)
        elif regex_match("你是谁", at_content):
            reply = who_r_u()
        elif at_content == "我爱你":
            reply = i_love_u(qq_number)
        elif at_content in ["我的cp是谁", "我的CP是谁"]:
            reply = my_cp(qq_number)
        elif regex_match('连接.+', at_content):
            reply = connect_server(at_content)
        elif at_content == "服务器时间":
            reply = server_time()
        elif regex_match('你在哪', at_content):
            reply = where_r_u(self)
        elif "是什么" in at_content or "是啥" in at_content:
            if check_ready(self.last_reply):
                self.last_reply = cur_time()
                reply = what_is(at_content)
            else:
                reply = "你发的太快啦！我处理不了这么多！"
        elif "长啥样" in at_content or "长什么样" in at_content:
            reply = what_is_image(at_content)
        elif at_content == "debug":
            if qq_number == PARTNER_QQ:
                self.debug = not self.debug
                reply = "Debug模式已更换为：{}！".format(str(self.debug))

        if reply is None:
            reply = self.mc_system.reply_group_at_msg(context, at_content)
        if reply is None:
            reply = self.ff_ststem.reply_group_at_msg(context, at_content)
        return reply

    async def reply_group_cmd_msg(self, bot, context, message):
        command = message[1:]
        par_list = command.split(' ')

        reply = None

        if par_list[0] == 'duel':
            reply = await duel(self, bot, context, par_list)

        elif par_list[0] == 'music':
            reply = music(par_list)

        elif par_list[0] == 'mc' and len(par_list) > 1 and context['group_id'] == int(SHADOWVILLAGE_QQ):
            reply = self.mc_system.reply_group_cmd_msg(context, par_list[1:])

        elif par_list[0] == 'ff' and len(par_list) > 1:
            reply = self.ff_ststem.reply_group_cmd_msg(context, par_list[1:])
        return reply


    def start(self):
        self.enable = True
        reply = "小紫已启动"
        return reply

    def close(self):
        self.enable = False
        reply = "小紫已关闭"
        return reply