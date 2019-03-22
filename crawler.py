from const import *

from selenium import webdriver
import random
import csv
import jieba


def get_driver(head=False):  # 得到驱动器
    if head:
        driver = webdriver.Chrome()
        return driver
    else:
        option = webdriver.ChromeOptions()
        option.add_argument('--no-sandbox')
        option.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=option)
        return driver


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


def search(message):
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

                if count >= len(new_list) / 2:
                    result_list.append(row)

    r = random.randint(0, len(result_list) - 1)
    return result_list[r]