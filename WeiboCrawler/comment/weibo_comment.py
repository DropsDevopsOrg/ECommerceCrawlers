#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2020/2/25 0025'

"""

import random
import time

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

from tools.mid_to_url import url_to_mid

# 要爬取热评的起始url
url = 'https://m.weibo.cn/comments/hotflow?id={id}&mid={mid}&max_id='
headers = {
    'Cookie': '你的cookie',
    'Referer': 'https://m.weibo.cn/detail/4281013208904762',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}




def get_page(max_id, id_type,mid):
    # 参数
    params = {
        'max_id': max_id,
        'max_id_type': id_type
    }
    try:
        r = requests.get(url.format(id=mid,mid=mid), params=params, headers=headers)
        print(r.url)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print('error', e.args)


def parse_page(jsondata):
    if jsondata:
        items = jsondata.get('data')
        item_max_id = {}
        item_max_id['max_id'] = items['max_id']
        item_max_id['max_id_type'] = items['max_id_type']
        item_max_id['max'] = items['max']
        return item_max_id


def write_csv(jsondata):
    datas = jsondata.get('data').get('data')
    for data in datas:
        created_at = data.get("created_at")
        like_count = data.get("like_count")
        source = data.get("source")
        floor_number = data.get("floor_number")
        username = data.get("user").get("screen_name")
        comment = data.get("text")
        comment = BeautifulSoup(comment, 'html.parser').get_text()
        print('当前楼层{},评论{}'.format(floor_number,comment))
        # print jsondata.dumps(comment, encoding="UTF-8", ensure_ascii=False)
        ws.append([username, created_at, like_count, floor_number, source,comment])



def run(url):
    # 输入来自微博采集的博客url链接，所有评论保存对应链接的xlsx

    m_id = 0
    id_type = 0
    mid=url_to_mid(url=url)
    jsondata = get_page(m_id, id_type,mid=mid)
    results = parse_page(jsondata)
    maxpage = results['max']
    print('多少页',maxpage)
    for page in range(maxpage):
        print('采集第{}页的微博'.format(page))
        jsondata = get_page(m_id, id_type,mid)
        print(jsondata)
        write_csv(jsondata)
        results = parse_page(jsondata)
        time.sleep(random.randint(2,4))
        wb.save('{}.xlsx'.format(url))
        if page%30==0:
            time.sleep(6)
        m_id = results['max_id']
        id_type = results['max_id_type']
    wb.save('{}.xlsx'.format(url))


if __name__ == '__main__':
    # 单个微博的采集：构造多线程、自动采集、快速采集根据自己情况更改
    i='IbhGya1EF'

    wb = Workbook()
    ws = wb.active
    print(i)
    try:
        run(url=i)
    except:pass

