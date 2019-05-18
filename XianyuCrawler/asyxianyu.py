#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/4/26 0026'
"""


import asyncio
import aiohttp
import time

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/4/24 0024'
"""
#-*- coding:utf-8 -*-
import time
import requests
import os
import json
import re
from pyquery import PyQuery as pq

import datetime
import threading
import random
from dingding import DingMsg
from db import MongoConfig,MongoProduct,MongoKeyword,MongoTime

class XianYu():
    def __init__(self,logMessage,errMessage):
        self.page = 1
        self.dbconf = MongoConfig()
        self.dbprod = MongoProduct()
        self.dbkey = MongoKeyword()
        self.dmes = DingMsg()
        self.finsh = False
        self.paginator_next = False
        self.data_list = []
        # self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.logMessage=logMessage
        self.errMessage=errMessage

    def range_webhook(self):
        webhook ='https://oapi.dingtalk.com/robot/send?access_token='+self.dbconf.select_all()[random.randint(0,self.dbconf.count()-1)].get('webhook')
        return webhook


    async def parse_html(self, html,keyword):
        print('开始解析')
        doc = pq(html)
        num = doc.find('.cur-num').text()   # 注释掉的参数为后续更改需求服务
        # print('总数',num)
        paginator_count = doc.find('.paginator-count').text()
        # paginator_pre = doc.find('.paginator-pre').text()
        self.paginator_next = doc.find('.paginator-next').text()  # 下一页
        now_page = doc.find('.paginator-curr').text()
        # print('现在在第几页',now_page)
        # P = '共([0-9]+)页'
        # all_pagenum = re.findall(P, paginator_count, re.S)
        # if all_pagenum:
        #     print(int(all_pagenum[0]))
        itmes = doc('#J_ItemListsContainer  .ks-waterfall').items()
        for item in itmes:
            data = {}
            data['keyword'] =keyword
            data['seller_nick'] = item.find('.seller-nick a').text()  # nick
            data['pic_href'] = 'https:'+str(item.find('.item-pic a').attr('href'))  # details_ulr
            data['title'] = item.find('.item-pic a').attr('title')  # title
            data['img_src'] = 'https:'+str(item.find('.item-pic a img').attr('data-ks-lazyload-custom'))  # img
            data['price'] = item.find('.item-attributes .item-price span em').text()  # price
            data['location'] = item.find('.item-attributes .item-location').text()
            data['desc'] = item.find('.item-brief-desc').text()
            data['pub_time'] = item.find('.item-pub-info .item-pub-time').text()
            data['add_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M-%S')
            #TODO：10分钟之内的商品采集

            try:
                if int(data.get('pub_time').replace('分钟前','')) > 10: # 大于20分之间隔时间判定为超时
                    continue
            except Exception as e: # 默认的时间大于及时了，直接舍弃
                continue

           # 如果数据库找不到对应关键字的链接 就插入数据，并且推送
            if not self.dbprod.select({"keyword":keyword,"pic_href":data.get('pic_href')}):
                self.dbprod.insert(data)
                self.logMessage.put('['+keyword+']['+data['pub_time']+']['+data['title']+'[')
                # print(data)

                # TODO：普通发消息
                # def send_message():
                #     if not getDingMes(webhook_url=self.range_webhook(), data=data,type=1):
                #         send_message()
                # send_message()
                # TODO: 链接发消息，不可取
                #TODO:markdown发消息

                self.markdown_list.append(data)
            else:
                print('数据已经存在mpass')
            print(data)
        print('#' * 50)

    async def get(self,url,payload):
        async with aiohttp.ClientSession() as session:
            async with session.get(url,params=payload) as resp:
                print(resp.status)
                print(resp.url)
                result = await resp.text()
        return result

    async def request(self,keyword_obj):
        keyword = keyword_obj.get('keyword')
        minPrice=keyword_obj.get('minPrice')
        maxPrice=keyword_obj.get('maxPrice')
        payload = {
            "st_edtime":1,  # 最新发布
            "_input_charset": "utf8",
            "search_type": "item",
            "q": keyword,
            "page": self.page,
            "start": minPrice,  # 价格范围
            "end": maxPrice,
        }
        url = 'https://s.2.taobao.com/list/'
        print('Waiting for', url)
        result = await self.get(url,payload)

        await self.parse_html(result,keyword)


    def run(self,type):
        self.markdown_list = []
        keywords = self.dbkey.select_all({'start':1})
        tasks = []
        for key_obj in keywords:
            tasks.append(asyncio.ensure_future(self.request(key_obj)))
        print(len(tasks))
        if tasks :
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            # 发送markdown数据文档，节约资源
            def send_message():
                if not self.dmes.send_msg(webhook_url=self.range_webhook(), data=self.markdown_list,type=type):
                    send_message()
                    self.errMessage.put('钉钉消息发送失败，发送数据太过于频繁')
                else:
                    self.errMessage.put('钉钉消息发送,使用类型{}'.format(type))
            if self.markdown_list:
                send_message()


def _run(logMessage,errMessage):

    # 这在tk线程中运行
    print('启动')
    dbtime = MongoTime()
    while True:
        time_config = dbtime.select_one({"flag":1})
        type =time_config.get('type')
        padding_time =time_config.get('time')
        start_time = time.time()
        xy = XianYu(logMessage,errMessage)
        xy.run(type)
        print('异步爬取用时：',time.time() - start_time )
        # TODO:配置中的时间
        errMessage.put('爬取耗时{}秒'.format(int(time.time() - start_time)))

        if not padding_time:
            padding_time = 10
        time.sleep(padding_time)

if __name__ == '__main__':
    from  multiprocessing import Process,JoinableQueue
    logMessage = JoinableQueue()
    errMessage = JoinableQueue()
    TProcess_crawler = threading.Thread(target=_run,args=(logMessage, errMessage))
    # TProcess_crawler.daemon = True
    TProcess_crawler.start()
    # TProcess_crawler.join()
    print('继续运行')