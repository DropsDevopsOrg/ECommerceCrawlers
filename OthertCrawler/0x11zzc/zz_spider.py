#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/6/22 0022'

"""
#多线程版本，速度有待提高

import time
from time import sleep
import requests
import threading
import queue
import random
import string
import re
from  html import unescape


class ZZSpider():
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
        }
        self.title_set = set()


    def generate_random_str(self, randomlength=6):
        """
        生成一个指定长度的随机字符串，其中
        string.digits=0123456789
        string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
        """
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
        random_str = ''.join(str_list)
        return random_str

    def fon_catalogue(self, base_url):
        front_url=self.generate_random_str(random.randint(3,5))
        return '{}{}/{}.html'.format(base_url, front_url, self.generate_random_str(7))

    def save_title(self,title):
        if title not in self.title_set:
            self.title_set.add(title)
            print(title)

    def req_title(self):
        '''
        传入网站url，解析网站的标题，加入到去重的队列函数中
        :return:
        '''
        while True:
            #暂停与启动

            flag = self.flag_queue.get()
            self.flag_queue.put(flag)
            if flag==0:
                time.sleep(2)
    # 内存中的数据,queue中的数据
            else:
                start_url = self.url_queue.get()
                try:
                    print(start_url)
                    self.logMessage.put(start_url)
                    req = requests.get(url=start_url, headers=self.headers)
                    encodings = requests.utils.get_encodings_from_content(req.text)
                    if encodings:
                        encoding = encodings[0]
                    else:
                        encoding = req.apparent_encoding
                    encode_content = req.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；
                    pattern = "<title>(.*?)</title>"
                    title = re.findall(pattern, encode_content)[0]
                    new_title=unescape(title)
                    self.logMessage.put(new_title)
                    self.save_title(title=new_title)
                except Exception as e:
                    print('解析错误：{}'.format(start_url))
                self.url_queue.task_done()
                time.sleep(self.timenum)


    def run(self,config,url_queue,flag_queue,logMessage,startBtn,stopBtn,tk):
        self.flag_queue=flag_queue
        self.url_queue=url_queue # 域名队列
        domain = config.get('domain')
        spidernum = config.get('spidernum')
        threadnum = config.get('threadnum')
        self.timenum = config.get('timenum')
        self.logMessage = logMessage
        path = config.get('path')

        for i in range(spidernum):
            reload_url = self.fon_catalogue(domain)  # 泛目录生成器，第一步暂时使用固定的数值进行解析
            self.url_queue.put(reload_url)

        thread_list = []

        for i in range(threadnum):
            Treq_title = threading.Thread(target=self.req_title)
            thread_list.append(Treq_title)
        for t in thread_list:
            t.setDaemon(True)
            t.start()
        for q in [self.url_queue]:
            q.join()
        print('结束')
        self.logMessage.put('数据采集结束')
        startBtn.config(state=tk.NORMAL, text='开始采集', bg='#F5F5F5', )
        stopBtn.config(state=tk.DISABLED, text='暂停采集', bg='#F5F5F5', )
        from export_title import EexportTxt
        et = EexportTxt()
        et.check_input_path(path)  # 检测输入的路径是否正确
        et.run(input_path=path, errMessage=logMessage, title_set=self.title_set)
        print(self.title_set)
        print('导出set中标题数据，300k为一个目标')
        self.logMessage.put('标题总数:{}'.format(len(self.title_set)))


if __name__ == '__main__':
    import time
    start_time=time.time()
    zzs = ZZSpider()
    config = {'threadnum': 2, 'timenum': 1, 'path': 'D:\\Python_program\\Spider\\zhizhu_spider\\titles', 'spidernum': 10, 'domain':  'http://richuriluo.qhdi.com/yl'}
    url_queue =queue.Queue()
    flag_queue =queue.Queue()
    flag_queue.queue.clear()
    flag_queue.put(1)
    logMessage =queue.Queue()


    t = threading.Thread(target=zzs.run, args=(config,url_queue,flag_queue,logMessage))
    t.start()

    print('下发完成')
    print('耗时:{}'.format(time.time()-start_time))

    def monitor_task():
        while True:

            start_url = url_queue.get()
            url_queue.put(start_url)
            print('进度条时间',url_queue.qsize())
            time.sleep(0.8)
            url_queue.task_done()
    def monior_thread():
        m = threading.Thread(target=monitor_task)
        m.setDaemon(True)
        m.start()
        url_queue.join()
    t = threading.Thread(target=monior_thread, )
    t.start()
    print(1)
