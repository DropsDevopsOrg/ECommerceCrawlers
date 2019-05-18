#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/5/9 0009'

"""

import re
import time
import threading
from souhu.parse_html import parse_souhu_news
import requests
from db import MongoUrl, MongoArticle


class NewsClawer():
    def __init__(self):
        self.dburl = MongoUrl()
        self.dbarticle = MongoArticle()
        self.url_set = set()

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.12 Safari/537.36"}

    def init_set(self):
        url_list = self.dburl.select({"flag": 1})
        for url in url_list:
            self.url_set.add(url.get('url'))

    def req_news_command(self):
        while True:
            start_url_obj = self.dburl.find_one_update_flag1()

            if not start_url_obj:
                print('url已经全部扫描完毕')
                time.sleep(50)
                continue
            start_url = start_url_obj.get('url')
            news_time = start_url_obj.get('time', '')
            news_title = start_url_obj.get('title', '')
            news_type = start_url_obj.get('type', '')

            print('起始url', start_url,news_type,news_time,news_title)
            try:
                req = requests.get(url=start_url,headers=self.headers, timeout=30)
                if req.status_code == 200:
                    if news_type == 'souhu':
                        article = parse_souhu_news(req)
                    elif news_type == 'baidu':
                        # 调用百度的解析
                        article = ''
                    else:  # 存在不明确的内容
                        article = ''
                    self.dbarticle.insert(
                        {"article": article, "flag": 0, "time": news_time, "url": start_url, "title": news_title,
                         "type": news_type})


                else:
                    print('请求请求不是200', )
                    self.dburl.update_url_flag0(start_url)
            except Exception as e:
                # 网站没有反爬。一般超时重新请求
                print('请求超时', e)
                self.dburl.update_url_flag0(start_url)

    def run(self):
        thread_list = []
        for i in range(11):
            Treq_page = threading.Thread(target=self.req_news_command)
            thread_list.append(Treq_page)
        for t in thread_list:
            # t.setDaemon(True)
            t.start()
            # t.join()


if __name__ == '__main__':
    nc = NewsClawer()
    nc.init_set()
    nc.run()
