# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
import os

import requests
from lxml import etree

from utils.utils import get_header
import queue
import csv

class LaGou(object):

    def __init__(self, keyword, city, path=os.getcwd()):
        self.keyword = keyword
        self.city = city
        self.csv_header = ['职位名称', '详细链接', '工作地点', '薪资', '公司名称', '经验要求', '学历', '福利', '职位信息']
        self.baseurl = 'https://www.lagou.com/jobs/positionAjax.json'
        self.path = path
        self.header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        self.data = queue.Queue()

    def Spider(self):
        for i in range(1, 31):
            s = requests.Session()
            s.get(
                url='https://www.lagou.com/jobs/list_运维?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
                headers=get_header(), timeout=3)
            cookie = s.cookies
            req = requests.post(self.baseurl, headers=self.header, data={'first': True, 'pn': i, 'kd': self.keyword},
                                params={'px': 'default', 'city': self.city, 'needAddtionalResult': 'false'},
                                cookies=cookie, timeout=3)
            text = req.json()
            datas = text['content']['positionResult']['result']
            for data in datas:
                s = requests.Session()
                s.get(
                    url='https://www.lagou.com/jobs/list_运维?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
                    headers=get_header(), timeout=3)
                cookie1 = s.cookies
                url = 'https://www.lagou.com/jobs/' + str(data.get('positionId')) + '.html'
                req1 = requests.get(url, headers=self.header, cookies=cookie1)
                req1.encoding = 'utf-8'
                html = etree.HTML(req1.text)
                detail = ''.join(html.xpath('//*[@class="job-detail"]//*/text()')).strip()
                if detail.isspace():
                    detail = ''.join(html.xpath('//*[@class="job-detail"]/text()')).strip()
                print(detail)
                data = {
                    "职位名称": data.get('positionName'),
                    "工作地点": data.get('district'),
                    "薪资": data.get('salary'),
                    "公司名称": data.get('companyFullName'),
                    "经验要求": data.get('workYear'),
                    "学历": data.get('education'),
                    "福利": data.get('positionAdvantage'),
                    "详细链接": url,
                    "职位信息": detail
                }
                self.data.put(data)

    def run(self):
        self.Spider()
        if os.path.exists(self.path):
            data_list = []
            self.path = os.path.join(self.path,'save-data')
            while not self.data.empty():
                data_list.append(self.data.get())
            with open(os.path.join(self.path, '拉钩网招聘_关键词_{}_城市_{}.csv'.format(self.keyword, self.city)), 'w',
                      newline='', encoding='utf-8-sig') as f:
                f_csv = csv.DictWriter(f, self.csv_header)
                f_csv.writeheader()
                f_csv.writerows(data_list)


if __name__ == '__main__':
    LaGou(keyword='java', city='北京').run()
