from selenium import webdriver
import time
import random


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


def get_real_answer(answer):  # 得到简化过的答案
    answer_text = answer.split("答：\n")[-1]
    answer_text.replace("请采纳", "")
    answer_text.replace("查看原帖>>", "")
    return answer_text


def auto_crawler(text):
    driver = get_driver(False)
    driver.get("https://zhidao.baidu.com/search?word=a")

    driver.find_element_by_id('kw').clear()
    driver.find_element_by_id('kw').send_keys("Minecraft " + text)
    driver.find_element_by_id('search-btn').click()
    time.sleep(2)

    body = driver.find_element_by_id('wgt-list')
    answer_list = body.find_elements_by_class_name('dl')
    r = random.randint(0, len(answer_list) - 1)
    answer = answer_list[r].find_element_by_class_name('answer').text
    answer = get_real_answer(answer)
    return answer
