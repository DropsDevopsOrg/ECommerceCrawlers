# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
import requests
import queue
import threading
import re
from lxml import etree
import csv
from copy import deepcopy

class KuAn(object):

    def __init__(self, type, page):
        self.type = type
        self.page = page
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
        self.csv_header = ['应用名称', '下载链接']
        with open('{}.csv'.format(self.type), 'a+', newline='', encoding='utf-8-sig') as f:
            csv_file = csv.writer(f)
            csv_file.writerow(self.csv_header)
        self.url = 'https://www.coolapk.com'
        self.base_url = 'https://www.coolapk.com/{}'.format(type)
        if type not in ['apk', 'game']:
            raise ValueError('type参数不在范围内')
        self.page_url_queue = queue.Queue()
        self.detail_url_queue = queue.Queue()
        self.save_queue = queue.Queue()

    def get_detail_url_fun(self):
        while True:
            page_url = self.page_url_queue.get()
            req = requests.get(url=page_url,headers=self.header)
            if req.status_code == 200:
                req.encoding = req.apparent_encoding
                html = etree.HTML(req.text)
                path = html.xpath('//*[@class="app_left_list"]/a/@href')
                for _ in path:
                    detail_url = self.url + _
                    print('正在获取详情链接:',detail_url)
                    self.detail_url_queue.put(deepcopy(detail_url))
            self.page_url_queue.task_done()

    def get_download_url_fun(self):
        while True:
            detail_url = self.detail_url_queue.get()
            req = requests.get(url=detail_url, headers=self.header)
            if req.status_code == 200:
                req.encoding = 'utf-8'
                url_reg = '"(.*?)&from=click'
                name_reg = '<p class="detail_app_title">(.*?)<'
                download_url = re.findall(url_reg, req.text)[0]
                name = re.findall(name_reg, req.text)[0]
                data = {'name': name, 'url': download_url}
                print('获取到数据:', data)
                self.save_queue.put(data)
            self.detail_url_queue.task_done()

    def save_data_fun(self):
        while True:
            data = self.save_queue.get()
            name = data.get('name')
            url = data.get('url')
            with open('{}.csv'.format(self.type), 'a+', newline='', encoding='utf-8-sig') as f:
                csv_file = csv.writer(f)
                csv_file.writerow([name, url])
            self.save_queue.task_done()


    def run(self):
        for _ in range(1, self.page+1):
            page_url = self.base_url + '?p={}'.format(_)
            print('下发页面url', page_url)
            self.page_url_queue.put(page_url)

        thread_list = []
        for _ in range(2):
            get_detail_url = threading.Thread(target=self.get_detail_url_fun)
            thread_list.append(get_detail_url)

        for _ in range(5):
            get_download_url = threading.Thread(target=self.get_download_url_fun)
            thread_list.append(get_download_url)

        for _ in range(2):
            save_data = threading.Thread(target=self.save_data_fun)
            thread_list.append(save_data)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for q in [self.page_url_queue, self.detail_url_queue, self.save_queue]:
            q.join()

        print('爬取完成，结束')

if __name__ == '__main__':

    a= KuAn(type='apk', page=302).run()

