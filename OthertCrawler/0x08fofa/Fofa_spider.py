#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/5/13 0013'

"""

import base64
import random
import time

import pymongo
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Fofa():
    def __init__(self,config):
        self.WRITE_MODE = config[
            'write_mode']  # 结果信息保存类型，为list形式，可包含txt、csv、json、mongo和mysql五种类型

        self.FOFA_USERNAME =config['fofa_username'] # fofa账号用户名
        self.FOFA_PASSWORD = config['fofa_password'] # fofa账号密码
        self.PAGE = config['page']

        self.MONGO_URL = 'localhost'
        self.MONGO_DB = 'fofa'
        self.MONGO_TABLE = 'message'

        self._init_db()
        self._init_browser()

    def _init_db(self):
        # 连接mongodb数据库
        client = pymongo.MongoClient(self.MONGO_URL)
        self.db = client[self.MONGO_DB]

    def _init_browser(self):

        # 初始化浏览器
        self.browser = webdriver.Chrome(service_args=['--load-images=false', '--disk-cache=true'])

        self.wait = WebDriverWait(self.browser, 10)
        self.browser.set_window_size(1400, 900)

    def login_fofa(self):
        try:
            self.browser.get('https://i.nosec.org/login?service=https%3A%2F%2Ffofa.so%2Fusers%2Fservice')
            input_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#username')))
            input_pass = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#password')))
            submit = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#login-form > table > tbody > tr:nth-child(4) > td > button')))
            input_user.send_keys(self.FOFA_USERNAME)
            input_pass.send_keys(self.FOFA_PASSWORD)
            submit.click()
            self.browser.implicitly_wait(30)
        except TimeoutException:
            return self.login_fofa()

    def turn_to_start_page(self):
        qbase = base64.b64encode(self.q.encode(encoding="utf-8"))
        starturl = 'https://fofa.so/result?page={}&qbase64={}#will_page'.format(self.now_page, str(qbase, 'utf-8'))
        self.browser.get(url=starturl)

    # 翻页操作
    def next_page(self):
        try:
            submit_next = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#will_page > a.next_page')))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ajax_content')))
            self.get_products()
            submit_next.click()
            # wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#will_page > em'),str(page_number))) # 很慢的
        except TimeoutException:
            print('循环下一页')
            return self.next_page()

    # 获取数据
    def get_products(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ajax_content')))
        except Exception as e:
            self.turn_to_start_page()
        # browser.implicitly_wait(30)
        html = self.browser.page_source
        doc = pq(html)
        items = doc('.list_main .list_mod_all #ajax_content .download_loader .list_mod').items()
        for item in items:
            product = {
                'url': item.find('.list_mod_t').text(),
                'info': item.find('.list_mod_c .row .col-lg-4 .list_sx1').text(),
                'flag': 0,
                'type': '博彩'
            }
            print(product)
            self.save_to_mongo(product)
            
#             # 保存格式为https:http ip port 任意组合形式 可以任意修改 现阶段为 http://domain:80 https://domain:443  domain:3389
#             url=  item.find('.list_mod_t').text()
#             url_list = url.split('\n')
#             domain=url_list[0]
#             port = url_list[1]
#             if port=='80':
#                 domain='http://'+domain
#             result = domain+':'+port+'\n'
#             self.save_text(result)


    def save_to_txt(self,result):
        # 应安全人员要求保存txt形式
        with open ('result.txt','a+')as f:
            f.write(result+'\n')
        pass
    # 存储到mongodb
    def save_to_mongo(self, result):
        try:
            if self.db[self.MONGO_TABLE].insert(result):
                pass
                # print('sucess', result)
        except Exception:
            print('faild', result)

    def main(self, q):
        self.login_fofa()
        self.q = q
        # search(str1)
        self.now_page = 1
        self.turn_to_start_page()
        for i in range(self.now_page, int(self.PAGE)):
            print('第多少页', i)
            self.now_page = i
            self.next_page()
            time.sleep(random.randint(3, 6))

        self.browser.quit()



import os
import sys
import json


def main():
    try:
        config_path = os.path.split(
            os.path.realpath(__file__))[0] + os.sep + 'config.json'
        if not os.path.isfile(config_path):
            sys.exit(u'当前路径：%s 不存在配置文件config.json' %
                     (os.path.split(os.path.realpath(__file__))[0] + os.sep))
        with open(config_path) as f:
            try:
                config = json.loads(f.read())
            except ValueError:
                sys.exit(u'config.json 格式不正确，请参考 ')
        fofa = Fofa(config)
        fofa.start()  # 爬取fofa信息
    except Exception as e:
        print('Error: ', e)



if __name__ == '__main__':
    main()
