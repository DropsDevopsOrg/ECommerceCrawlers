#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2020/2/25 0025'

"""

import random
import requests
import time
import os
import csv
import codecs
import sys
import json
from bs4 import BeautifulSoup
from tools.mid_to_url import url_to_mid

from openpyxl import Workbook

# 要爬取热评的起始url
url = 'https://m.weibo.cn/api/statuses/repostTimeline'
headers = {
    'Cookie': '你的cookie',
    'Referer': 'https://m.weibo.cn/detail/4281013208904762',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}




def get_page(id, page):
    # 参数
    params = {
        'id': id,
        'page': page
    }
    try:
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print('error', e.args)


def write_csv(jsondata):
    datas = jsondata.get('data').get('data')
    for data in datas:
        created_at = data.get("created_at")

        source = data.get("source")

        username = data.get("user").get("screen_name")
        comment = data.get("text")
        comment = BeautifulSoup(comment, 'html.parser').get_text()
        print(',评论{}'.format(comment))
        ws.append([username, created_at, source, comment ])


def run(url):
    # 存为xlsx

    mid = url_to_mid(url=url)
    jsondata = get_page(mid, 1)
    maxpage = jsondata['data']['max']

    for page in range(1, maxpage):
        jsondata = get_page(mid, page)
        print(maxpage,page)
        try:
            write_csv(jsondata)
        except:
            break
        time.sleep(random.randint(2, 5))
        if page % 30 == 0:
            time.sleep(60)
            wb.save('{}.xlsx'.format(url))
    wb.save('{}.xlsx'.format(url))

if __name__ == '__main__':
    # 单个微博的采集：构造多线程、自动采集、快速采集根据自己情况更改
    i='IbhGya1EF'
    wb = Workbook()
    ws = wb.active
    run(url=i)
