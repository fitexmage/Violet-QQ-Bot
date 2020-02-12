from config import *

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import random
import re
import csv
import time
import jieba


def get_driver(head=False):  # 得到驱动器
    if head:
        driver = webdriver.Chrome()
        return driver
    else:
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "none"
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        return driver

# For MC

def get_new_url():
    data = []
    with open(raw_url_path) as f:
        count = 1
        reader = csv.reader(f)
        for row in reader:
            print(count)
            count += 1
            title = row[2].replace("Minecraft(我的世界)中文论坛 - ", "")
            array = title.split("\xa0-\xa0")
            title = array[0]
            row[2] = title
            if len(array) > 1:
                type = array[1]
                row.append(type)
            data.append(row)

    with open('data/new_url.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)


def load_stopwords():
    stopwords_set = set()
    with open(stopwords_path) as f:
        words = f.read().splitlines()
    for word in words:
        stopwords_set.add(word)
    return stopwords_set


def search_url(message):
    stopwords_set = load_stopwords()

    list = jieba.cut(message, cut_all=False)
    new_list = []
    for word in list:
        if word not in stopwords_set:
            new_list.append(word)

    result_list = []
    with open(new_url_path) as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 4 and row[3] in question_set:
                count = 0
                for word in new_list:
                    if word in row[2]:
                        count += 1

                if count >= len(new_list) * 0.6:
                    result_list.append((row, count))

    if len(result_list) > 0:
        result_list.sort(key=lambda count: count[1], reverse=True)
        r = random.randint(0, len(result_list) - 1 if len(result_list) <= 100 else 100)
        return result_list[r][0][1]
    return None


def crawler_result(url):
    try:
        driver = get_driver(False)
        driver.get(url)
        time.sleep(1)
        post_list = driver.find_element_by_id('postlist').find_elements_by_class_name('plhin')

        if len(post_list) > 1:
            author = post_list[0].find_element_by_class_name('authi').text

            for i in range(5):
                r = random.randint(1, len(post_list) - 1)
                post = post_list[r]
                if author is not post.find_element_by_class_name('authi').text:
                    reply = post.find_element_by_class_name('t_f').text
                    reply = re.sub(".* 发表于 [0-9]*-[0-9]*-[0-9]* [0-9]*:[0-9]*", "", reply)
                    reply = re.sub("本帖最后由 .* 于 [0-9]*-[0-9]*-[0-9]* [0-9]*:[0-9]* 编辑", "", reply)
                    reply = re.sub("登录/注册后可看大图", "", reply)
                    reply = reply.strip()
                    if re.match('http.*', reply) is None:
                        return reply
    except:
        pass
    return None


def get_combat_data(command):
    par_list = command.split(' ')
    if len(par_list) != 3:
        return None
    type = par_list[0]
    dungeon = par_list[1]
    role = par_list[2]

    if type != 'dps' and dungeon not in dungeon_dict or role not in role_dict:
        return None

    driver = get_driver(False)
    driver.get("https://cn.fflogs.com/zone/statistics/{}&dpstype=adps&class=Global&spec={}&dataset=100"
               .format(dungeon_dict[dungeon][1], role_dict[role][1]))

    time.sleep(3)

    rect = driver.find_element_by_id('highcharts-0')\
        .find_element_by_class_name('highcharts-series-group')\
        .find_element_by_class_name('highcharts-series')\
        .find_elements_by_tag_name('rect')

    reply = '{} {}(adps)'.format(dungeon_dict[dungeon][0], role_dict[role][0])
    for i in range(len(rect)):
        driver.execute_script("var q=document.documentElement.scrollTop=300")
        ActionChains(driver).move_to_element(rect[i]).perform()
        data = driver.find_element_by_id('highcharts-0')\
        .find_elements_by_class_name('highcharts-tooltip')[-1]\
        .find_element_by_tag_name('b').text
        reply += '\n{}：{}'.format(level_dict[i], data)

    return reply