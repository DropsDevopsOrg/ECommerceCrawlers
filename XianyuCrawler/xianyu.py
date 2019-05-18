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
import pandas as pd
import datetime

class XianYu():
    def __init__(self):
        self.page = 1
        self.finsh = False
        self.paginator_next = False
        self.data_list = []
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.header = ['用户昵称', '会员等级', '详情链接', '商品标题', '图片链接', '价格', '地址', '描述', '时间{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '留言']

    def crawler(self):
        payload = {
            "st_edtime ": 1,  # 最新发布
            "_input_charset": "utf8",
            "search_type": "item",
            "q": self.keyword,
            "page": self.page
            # "start": minPrice,  # 价格范围
            # "end": maxPrice,
        }
        # https://s.2.taobao.com/list/?q=%E4%B9%92%E4%B9%93%E7%90%83%E6%8B%8D&ajax=true&page=2&search_type=item&_input_charset=utf8
        try:
            rep = requests.get(url="https://s.2.taobao.com/list/?", params=payload)
            rep.encoding = rep.apparent_encoding
            res = rep.text
            return res
        except Exception as e:
            print('error' * 22)
            return False

    def parse_html(self, html):
        doc = pq(html)
        paginator_count = doc.find('.paginator-count').text()
        # paginator_pre = doc.find('.paginator-pre').text()
        self.paginator_next = doc.find('.paginator-next').text()  # 下一页
        now_page = doc.find('.paginator-curr').text()
        print(now_page)
        P = '共([0-9]+)页'
        all_pagenum = re.findall(P, paginator_count, re.S)
        if all_pagenum:
            print(int(all_pagenum[0]))
        itmes = doc('#J_ItemListsContainer  .ks-waterfall').items()
        for item in itmes:
            data = {}
            data['a_seller_nick'] = item.find('.seller-nick a').text()  # nick
            data['b_seller_icons'] = item.find('.seller-icons').text()  # vip classes
            data['c_pic_href'] = item.find('.item-pic a').attr('href')  # details_ulr
            data['d_title'] = item.find('.item-pic a').attr('title')  # title
            data['e_img_src'] = item.find('.item-pic a img').attr('data-ks-lazyload-custom')  # img
            data['f_price'] = item.find('.item-attributes .item-price span em').text()  # price
            data['g_location'] = item.find('.item-attributes .item-location').text()
            data['h_desc'] = item.find('.item-brief-desc').text()
            data['i_pub_time'] = item.find('.item-pub-info .item-pub-time').text()
            data['j_other_info'] = item.find('.item-other-info a em').text()
            if data['d_title']:
                self.data_list.append(data)
                print(data)
        print('#' * 50)

    def save_CSV(self):
        print('写入数据')
        data = pd.DataFrame(self.data_list)
        csv_filename = os.path.join(self.base_path, 'temp', '{}.csv'.format(keyword))
        data.to_csv(csv_filename, header=self.header, index=False, mode='a+', encoding='utf_8_sig')

    def run(self, keyword):
        self.keyword = keyword
        while not self.finsh:
            content_html = self.crawler()
            if content_html:
                self.parse_html(content_html)
                if self.paginator_next:
                    self.page += 1
                else:
                    self.finsh = True
                # if self.page==300:
                #     self.finsh = True
        self.save_CSV()


if __name__ == '__main__':
    if not os.path.exists('temp'):
        os.mkdir('temp')
    start_time = time.time()
    keywords = ['羽毛球拍', 'iphone']
    for keyword in keywords:
        xy = XianYu()
        xy.run(keyword=keyword)
    print('单线程爬取用时：', time.time() - start_time)
