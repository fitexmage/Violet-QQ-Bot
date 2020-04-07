from config import *

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from bs4 import BeautifulSoup
import random
import re
import csv
import time
import jieba
import urllib.parse
import json


def get_driver(head=False, wait=True):  # 得到驱动器
    if head:
        driver = webdriver.Chrome()
        return driver
    else:
        if not wait:
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities["pageLoadStrategy"] = "none"
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=options)
        return driver

# For MC

# def get_new_url():
#     data = []
#     with open(RAW_URL_PATH) as f:
#         count = 1
#         reader = csv.reader(f)
#         for row in reader:
#             print(count)
#             count += 1
#             title = row[2].replace("Minecraft(我的世界)中文论坛 - ", "")
#             array = title.split("\xa0-\xa0")
#             title = array[0]
#             row[2] = title
#             if len(array) > 1:
#                 type = array[1]
#                 row.append(type)
#             data.append(row)
#
#     with open('data/new_url.csv', 'w', newline='') as f:
#         writer = csv.writer(f)
#         for row in data:
#             writer.writerow(row)
#
#
# def load_stopwords():
#     stopwords_set = set()
#     with open(STOPWORDS_PATH) as f:
#         words = f.read().splitlines()
#     for word in words:
#         stopwords_set.add(word)
#     return stopwords_set
#
#
# def search_url(message):
#     stopwords_set = load_stopwords()
#
#     list = jieba.cut(message, cut_all=False)
#     new_list = []
#     for word in list:
#         if word not in stopwords_set:
#             new_list.append(word)
#
#     result_list = []
#     with open(NEW_URL_PATH) as f:
#         reader = csv.reader(f)
#         for row in reader:
#             if len(row) == 4 and row[3] in question_set:
#                 count = 0
#                 for word in new_list:
#                     if word in row[2]:
#                         count += 1
#
#                 if count >= len(new_list) * 0.6:
#                     result_list.append((row, count))
#
#     if len(result_list) > 0:
#         result_list.sort(key=lambda count: count[1], reverse=True)
#         r = random.randint(0, len(result_list) - 1 if len(result_list) <= 100 else 100)
#         return result_list[r][0][1]
#     return None
#
#
# def crawl_result(url):
#     try:
#         driver = get_driver(False)
#         driver.get(url)
#         time.sleep(1)
#         post_list = driver.find_element_by_id('postlist').find_elements_by_class_name('plhin')
#
#         if len(post_list) > 1:
#             author = post_list[0].find_element_by_class_name('authi').text
#
#             for i in range(5):
#                 r = random.randint(1, len(post_list) - 1)
#                 post = post_list[r]
#                 if author is not post.find_element_by_class_name('authi').text:
#                     reply = post.find_element_by_class_name('t_f').text
#                     reply = re.sub(".* 发表于 [0-9]*-[0-9]*-[0-9]* [0-9]*:[0-9]*", "", reply)
#                     reply = re.sub("本帖最后由 .* 于 [0-9]*-[0-9]*-[0-9]* [0-9]*:[0-9]* 编辑", "", reply)
#                     reply = re.sub("登录/注册后可看大图", "", reply)
#                     reply = reply.strip()
#                     if re.match('http.*', reply) is None:
#                         return reply
#     except:
#         pass
#     return None


def get_real_answer(answer):  # 得到简化过的答案
    answer_text = answer.split("答：\n")[-1]
    answer_text.replace("请采纳", "")
    answer_text.replace("查看原帖>>", "")
    return answer_text


def crawl_zhidao(content):
    reply = None

    if len(content) >= 30:
        sent_list = re.split(r'[,.!?，。！？、]', content)
        for sent in sent_list:
            if len(sent) <= 30 and sent != "":
                content = sent
        if len(content) >= 30:
            return reply

    driver = get_driver()
    try:
        driver.get(ZHIDAO_URL + content)
        body = driver.find_element_by_id('wgt-list')
        answer_list = body.find_elements_by_class_name('dl')
        answer_list = random.sample(answer_list, k=len(answer_list) * 2 // 3)
    except:
        return reply

    for answer in answer_list:
        question = answer.find_element_by_class_name('ti').text
        if content in question:
            answer_text = answer.find_element_by_class_name('answer').text
            answer_text = get_real_answer(answer_text)
            if len(answer_text) >= 30:
                sent_list = re.split(r'[,.!?，。！？、]', answer_text)
                sent_list = random.sample(sent_list, k=3)
                for sent in sent_list:
                    if len(sent) <= 30 and sent != "":
                        reply = sent
                        break
                if reply is None:
                    continue
                else:
                    break
            reply = answer_text
            break
    driver.delete_all_cookies()
    driver.quit()
    return reply


def crawl_baike(item):
    driver = get_driver()
    try:
        driver.get(BAIKE_URL + item)
        time.sleep(1)
        content = driver.find_element_by_class_name('content-wrapper').find_element_by_class_name('lemma-summary')
        content = content.text.split('\n')[0]
        reply = re.sub('\[.*\]', '', content)
    except:
        reply = "好像……没听说过这个"
    driver.delete_all_cookies()
    driver.quit()
    return reply


def crawl_image(item):
    if item == '小紫':
        reply = generate_image_cq(AVATAR_PATH + 'violet.jpeg')
        return reply
    elif item in ['腐竹', '夏月'] :
        reply = generate_image_cq(AVATAR_PATH + 'myself.jpeg')
        return reply

    wb_data = requests.get(IMAGE_URL + 'q={}&src=srp&correct=&sn=&pn=60'.format(item))
    image_list = json.loads(wb_data.text)['list']
    if len(image_list) == 0:
        reply = "好像……没听说过这个"
        return reply
    url_list = []
    for image in image_list:
        url = image['img']
        image_size = image['imgsize']
        if int(float(image_size.replace('KB', ''))) < 60:
            url_list.append(url)

    if len(url_list) != 0:
        image_url = random.choice(url_list)
        print(image_url)
        reply = generate_image_cq(image_url)
    else:
        reply = '图片都好大，顶不住了……'
    return reply


def crawl_music(music_name):
    wb_data = requests.get(NETEASE_MUSIC_URL + music_name)
    data = json.loads(wb_data.text)
    if data['code'] != 200 or data['result']['songCount'] == 0:
        reply = "好像……没听说过这首歌"
    else:
        music_id = json.loads(wb_data.text)['result']['songs'][0]['id']
        reply = generate_music_cq(music_id, '163')
    return reply


def crawl_dps(server, dungeon, role):
    if server == "国际服":
        server= DPS_DUNGEON_DICT[dungeon]['global_server']
    else:
        server= DPS_DUNGEON_DICT[dungeon]['cn_server']

    fflogs_url = "https://www.fflogs.com/zone/statistics/table/{}/dps/{}/{}/8/{}/100/1000/7/0/Global/{}/All/0/normalized/single/0/-1/?keystone=15&dpstype=adps" \
        .format(DPS_DUNGEON_DICT[dungeon]['quest'], DPS_DUNGEON_DICT[dungeon]['id'], DPS_DUNGEON_DICT[dungeon]['difficulty'], server, ROLE_DICT[role]['attr'])

    s = requests.Session()
    s.headers.update({'referer': FFLOGS_URL})
    try:
        r = s.get(url=fflogs_url, timeout=10)
    except:
        return []
    dps_list = []
    for level in LEVEL_LIST:
        if level == "100":
            str = ("series" + r".data.push\(([0-9]+(\.[0-9])*)")
        else:
            str = ("series%s" % (level) + r".data.push\(([0-9]+(\.[0-9])*)")
        dps = re.compile(str).findall(r.text)[-1][0]
        dps_list.append(dps)
    return dps_list


def crawl_item(item):
    if len(item) > 20:
        reply = "你确定有名字这么长的物品吗……"
        return reply
    url = WIKI_URL + urllib.parse.quote("物品") + ":" + urllib.parse.quote(item)
    wb_data = requests.get(url)
    bs = BeautifulSoup(wb_data.text, "html.parser")
    content = bs.find(attrs={'class':"noarticletext"})
    if content is None:
        content = bs.find(attrs={'class': "ff14-content-box-block"}).text[4:]
        image = bs.find(attrs={"property": "og:image"})['content']
        reply = "[CQ:share,url={},title={},content={},image={}]".format(url, item, content, image)
    else:
        url = WIKI_URL + "ItemSearch?name=" + urllib.parse.quote(item)
        driver = get_driver()
        try:
            driver.get(url)
            time.sleep(1)
            content = driver.find_element_by_id('mw-content-text').find_element_by_class_name('mw-parser-output')
            if "没有" not in content.text:
                reply = '[CQ:share,url={},title="{}"的搜索结果]'.format(url, item)
            else:
                reply = '没有找到与"{}"相关的物品。'.format(item)
        except:
            reply = "服务器繁忙，请稍候再试！"
        driver.delete_all_cookies()
        driver.quit()
    return reply


def crawl_dungeon(dungeon):
    if len(dungeon) > 30:
        reply = "你确定有这么长名字的副本吗……"
        return reply
    elif dungeon == '塔塔露歼殛战':
        url = "https://www.baidu.com/s?wd=%E5%A4%A7%E8%83%83%E7%8E%8B%E6%AF%94%E8%B5%9B"
        reply = "[CQ:share,url={},title={}]".format(url, dungeon)
        return reply
    url = WIKI_URL + urllib.parse.quote(dungeon)
    wb_data = requests.get(url)
    bs = BeautifulSoup(wb_data.text, "html.parser")
    no_text = bs.find(attrs={'class': "noarticletext"})
    if no_text is None:
        content = bs.find(attrs={'class': "ff14-content-box-block"})
        if content is None:
            content = ''
            try:
                image = bs.find(attrs={'class': "image"}).find('img')['src']
            except:
                image = ''
        else:
            content = content.text[4:]
            image = bs.find(attrs={'class': "instance-infobox--banner"}).find('img')['src']
        reply = "[CQ:share,url={},title={},content={},image={}]".format(url, dungeon, content, image)
    else:
        reply = "副本名称错误！"
    return reply


def crawl_nuannuan():
    url = NUANNUAN_URL
    r = requests.get(url=url, timeout=5)
    data = json.loads(r.text)
    if data['success']:
        reply = data['content']
    else:
        reply = "暖暖崩了，请稍候再试~"
    return reply
