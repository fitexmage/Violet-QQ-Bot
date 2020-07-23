from ff_util import *
from config import *
from util import *
from crawler import crawl_item, crawl_nuannuan


class FF_System:
    def __init__(self):
        self.luck_dict = load_file(FF_LUCK_PATH)

    def reply_intro(self):
        reply = intro()
        return reply

    def reply_private_msg(self, context):
        message = context['message']
        qq_number = str(context['sender']['user_id'])

        reply = None

        return reply

    def reply_group_at_msg(self, context, at_content):
        qq_number = str(context['sender']['user_id'])

        reply = None

        if at_content in {"最终幻想14", "ff14"}:
            reply = self.reply_intro()

        return reply

    def reply_group_cmd_msg(self, context, par_list):
        qq_number = str(context['sender']['user_id'])
        func = par_list[0]
        # Don't remove the first parameter, cause some command only have the first one

        reply = None

        if func == "help":
            reply = intro()
        elif func == "dps":
            reply = dps(par_list)
        elif func == "dice":
            reply = dice(par_list)
        elif func == "gate":
            reply = gate(par_list)
        elif func == "占卜":
            reply = luck(self, qq_number)
        elif func == "item":
            if len(par_list) > 1:
                item = par_list[1]
                reply = crawl_item(item)
        elif func == "dungeon":
            reply = dungeon(par_list)
        elif func == "nuannuan":
            reply = crawl_nuannuan()
        elif func == "fish":
            reply = fish(par_list)
        elif func == "house":
            reply = house(par_list)
        elif func == "tianshu":
            reply = tianshu(par_list)
        elif func == "market":
            reply = market(par_list)
        return reply

