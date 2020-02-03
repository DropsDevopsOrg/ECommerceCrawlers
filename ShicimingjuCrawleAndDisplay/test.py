#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2020/2/1 0001'

"""
import queue
import re
import threading

import requests
from faker import Faker
from lxml import etree
user_agent = Faker('zh-CN').user_agent()
def get_header():
    return {
        'User-Agent': user_agent,
        'Connection': 'close'
    }

class Shici(object):

    def __init__(self, thread=1):
        self.poet_queue = queue.Queue()  # 诗人
        self.thread = thread
        self.base_url = 'http://www.shicimingju.com'

    def get_poet_url(self):
        for i in range(1, 13054):
            url = 'http://www.shicimingju.com/chaxun/zuozhe/{}.html'.format(i)

            self.poet_queue.put(url)

    def Spider(self):
        while not self.poet_queue.empty():
            url = self.poet_queue.get()
            req = requests.get(url, headers=get_header())
            if req.status_code == 200:
                req.encoding = 'utf-8'
                html = etree.HTML(req.text)
                # print(req.text)
                print(url)
                name = html.xpath('/html/body/div[4]/div[2]/div[2]/div[1]/h2/a/text()')[0]
                dynasty = html.xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/text()')
                if len(dynasty) == 0:
                    dynasty = '未知'
                else:
                    dynasty = dynasty[0]
                introduction = html.xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[4]')[0].xpath(
                    'string(.)').strip()


                poem_num = html.xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[3]/text()')[0][:-1]
                poet_url_list = []
                for i in range(1, int(int(poem_num) / 40) + 2):
                    poet_id = re.sub("\D", "", url)
                    poet_page_url = 'http://www.shicimingju.com/chaxun/zuozhe/{}_{}.html'.format(poet_id, i)
                    req1 = requests.get(url=poet_page_url, headers=get_header())
                    if req1.status_code == 200:
                        req1.encoding = 'utf-8'
                        list_html = etree.HTML(req1.text)
                        poet_url = list_html.xpath('//*/h3/a/@href')
                        poet_url_list += poet_url
                poet_url_list = map(lambda x: self.base_url + x, poet_url_list)
                for url in poet_url_list:
                    print(url)
                    req2 = requests.get(url, headers=get_header())
                    if req2.status_code == 200:
                        req2.encoding = 'utf-8'
                        poet_html = etree.HTML(req2.text)
                        title = poet_html.xpath('//*[@class="shici-title"]/text()')[0]
                        content = '\n'.join(poet_html.xpath('//*[@class="shici-content"]/text()')).strip()
                        if not content:
                            content = '\n'.join(poet_html.xpath('//*[@class="para"]/text()')).strip()
                        if len(poet_html.xpath('//*[@class="shangxi-container"]')) == 0:
                            analysis = ''
                        else:
                            analysis = poet_html.xpath('//*[@class="shangxi-container"]')[0].xpath(
                                'string(.)').strip()


    def run(self):
        self.get_poet_url()
        thread_list = []
        for i in range(self.thread):
            t = threading.Thread(target=self.Spider)
            thread_list.append(t)
        for t in thread_list:
            t.setDaemon(True)
            t.start()
        for t in thread_list:
            t.join()
        self.Spider()


a = Shici()
a.run()