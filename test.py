from selenium import webdriver
import re

from selenium.common.exceptions import TimeoutException


def get_driver(head=False):  # 得到驱动器
    if head:
        driver = webdriver.Chrome()
        return driver
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        return driver

def crawler_mcmod(question):
    driver = get_driver(False)
    driver.set_page_load_timeout(5)
    try:
        driver.get("http://www.mcmod.cn/s?key=" + question + "&filter=2")
    except TimeoutException:
        pass
    try:
        result_list = driver.find_element_by_class_name('search-result-list')
        results = result_list.find_elements_by_class_name('result-item')
        head = None
        for result in results:
            body = result.find_element_by_class_name('body')
            if body.text != "":
                head = result.find_element_by_class_name('head')
                break
        if head is None:
            return None
        mod = re.search('- (.*)', head.text).group(1)
        head.find_element_by_tag_name('a').click()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        try:
            answer = driver.find_element_by_class_name('item-content').text
        except TimeoutException:
            answer = driver.find_element_by_class_name('item-content').text
        answer = "在" + mod + "中：\n" + answer
        return answer
    except Exception:
        return None

print(crawler_mcmod("工业作物收割机"))