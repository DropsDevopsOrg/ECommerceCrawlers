#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/5/9 0009'

"""
from urllib.parse import urlparse
from souhu.config import size, type_name, new_url_list
from db import MongoArticle, MongoUrl
import requests
import time
import datetime
import threading
import queue

from urllib import parse


class SouhuSpider():
    def __init__(self):
        self.dburl = MongoUrl()
        self.dbarticle = MongoArticle()
        self.url_set = set()
        self.url_queue = queue.Queue()
        self.init_set()

    def init_set(self):
        url_list = self.dburl.select({"type": type_name})
        for url in url_list:
            self.url_set.add(url.get('url'))
    def strf_time(self,timeStamp):
        if timeStamp is None:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        localTime = time.localtime(int(timeStamp)/1000)
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
        return strTime
    def req_json(self):
        while True:
            start_url = self.url_queue.get()
            try:
                # if 1==1:
                req = requests.get(url=start_url, timeout=30)
                if req.status_code != 200:
                    print('网站拒绝访问')
                souhu_json = req.json()
                news_header_list = souhu_json.get('data')
                if news_header_list:
                    for per_new in news_header_list:
                        if not per_new.get("url"):
                            continue  # 没有url则继续下一个
                        if urlparse(per_new.get('url')).scheme == 'https':
                            continue  # 没有http则是广告
                        url = parse.urljoin('http://m.sohu.com', per_new.get("url"))
                        title = per_new.get("title")
                        publicTime = per_new.get("publicTime")
                        url_time = self.strf_time(publicTime)  # 时间格式为
                        # 如果时间不大于当天的日期，则进行下一次
                        if url not in self.url_set:
                            self.url_set.add(url)
                            print(url)
                            self.logMessage.put('【新闻】【{}】{}'.format(url_time,title))
                            print('新增数据：', title)
                            self.dburl.insert(
                                {"url": url, "time": url_time, "flag": 0, "title": title, "type": type_name})
            except Exception as e:
                # 网站没有反爬。一般超时重新请求
                print('请求超时', e)
                self.url_queue.put(start_url)
            self.url_queue.task_done()

    def run(self,logMessage,errMessage):
        self.logMessage=logMessage
        self.errMessage=errMessage
        # "http://v2.sohu.com/integration-api/mix/region/84?size=100",
        for base_url in new_url_list:
            for i in range(1, 130):
                if i==87:
                    continue
                new_url = '{base_url}{i}?size={size}'.format(base_url=base_url, i=str(i), size=size)
                # if new_url not  in self.url_set:
                #     self.url_set.add(new_url)
                self.url_queue.put(new_url)

        thread_list = []
        for i in range(11):
            Treq_page = threading.Thread(target=self.req_json)
            thread_list.append(Treq_page)
        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for q in [self.url_queue]:
            q.join()
        print('结束')
if __name__ == '__main__':
    ss = SouhuSpider()
    while True:
        ss.run()
        time.sleep(60)
