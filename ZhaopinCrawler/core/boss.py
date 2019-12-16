# -*- coding: UTF-8 -*-
__author__ = 'Joynice'

import csv
import os
import queue

import requests
from lxml import etree

from utils.utils import get_header


class Boss(object):
    '''
    Boss直聘
    '''

    def __init__(self, keyword, city, path=os.getcwd()):
        self.keyword = keyword
        self.city = city
        self.path = path
        self.base_url = 'https://www.zhipin.com/mobile/jobs.json'  #手机端接口没有验证
        self.csv_header = ['职位名称', '职位链接', '公司名称', '工作地点', '薪资', '工作经验', '学历要求',]

    def _get_city_code(self):
        url = 'https://www.zhipin.com/wapi/zpCommon/data/city.json'
        headers = get_header()
        req = requests.get(url=url, headers=headers).json()
        if req['message'] == 'Success':
            city_code_dict = req.get('zpData').get('cityList')
            for i in city_code_dict:
                for c in i['subLevelModelList']:
                    if c['name'] == self.city:
                        return str(c['code'])
            return '100010000'  # 全国

    def Spider(self):
        page = 1
        city = self._get_city_code()
        data = []
        while 1:
            params = {
                'query': self.keyword,
                'page' : page,
                'city': city
            }
            req = requests.get(url=self.base_url, params=params, headers=get_header())
            print(req.url)
            req.encoding = req.apparent_encoding
            code = req.json().get('html')
            if code:
                html = etree.HTML(code)
                title = html.xpath('//*[@class="title"]/h4/text()')
                href = map(lambda x: 'https://www.zhipin.com'+x, html.xpath('//*[@class="item"]/a/@href'))
                salary = html.xpath('//*[@class="salary"]/text()')
                company = html.xpath('//*[@class="name"]/text()')
                area = html.xpath('//*[@class="msg"]/em[1]/text()')
                workingExp = html.xpath('//*[@class="msg"]/em[2]/text()')
                eduLevel = html.xpath('//*[@class="msg"]/em[3]/text()')
                for t,s,c,a,w,e,h in zip(title, salary, company, area, workingExp, eduLevel, href):
                    job = {}
                    job['职位名称'] = t
                    job['职位链接'] = h
                    job['公司名称'] = c
                    job['工作地点'] = a
                    job['薪资'] = s
                    job['工作经验'] = w
                    job['学历要求'] = e
                    data.append(job)
                page += 1
            else:
                break
        return data


    def run(self):
        if os.path.exists(self.path):
            self.path = os.path.join(self.path, 'save-data')
            data = self.Spider()
            print(data)
            with open(os.path.join(self.path, 'Boss直聘_关键词_{}_城市_{}.csv'.format(self.keyword, self.city)), 'w',
                      newline='', encoding='gb18030') as f:
                f_csv = csv.DictWriter(f, self.csv_header)
                f_csv.writeheader()
                f_csv.writerows(data)

if __name__ == '__main__':
    a = Boss(keyword='java', city='南京').run()
