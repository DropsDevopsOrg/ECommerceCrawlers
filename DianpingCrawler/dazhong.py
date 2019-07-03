#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/3/21 0021'

"""
import datetime
import random
import re
import time

import requests
from lxml import etree


class DianpingComment:
    font_size = 14
    start_y = 23

    def __init__(self, shop_id, cookies, delay=7):
        self.shop_id = shop_id
        self._delay = delay
        self.font_dict = {}
        self._cookies = self._format_cookies(cookies)
        self._css_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        }
        self._default_headers = {
            'Connection': 'keep-alive',
            'Host': 'www.dianping.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        }
        self._cur_request_url = 'http://www.dianping.com/shop/{}/review_all/p1'.format(shop_id)
        self._cur_request_css_url = 'http://www.dianping.com/shop/{}/'.format(shop_id)

    def _delay_func(self):
        delay_time = random.randint((self._delay - 2) * 10, (self._delay + 2) * 10) * 0.1
        print('睡一会', delay_time)
        time.sleep(delay_time)

    def _format_cookies(self, cookies):
        cookies = {cookie.split('=')[0]: cookie.split('=')[1]
                   for cookie in cookies.replace(' ', '').split(';')}
        return cookies

    def _get_css_link(self, url):
        """
            请求评论首页，获取css样式文件
        """
        res = requests.get(self._cur_request_css_url, headers=self._default_headers, cookies=self._cookies)
        html = res.text
        print('首页源码',html)
        # css_link = re.search(r'<link re.*?css.*?href="(.*?svgtextcss.*?)">', html)
        css_link = re.findall(r'<link rel="stylesheet" type="text/css" href="//s3plus.meituan.net/v1/(.*?)">', html)
        assert css_link
        css_link = 'http://s3plus.meituan.net/v1/' + css_link[0]
        print('css链接',css_link)
        return css_link



    def _get_font_dict_by_offset(self, url):
        """
            获取坐标偏移的文字字典, 会有最少两种形式的svg文件（目前只遇到两种）
        """
        res = requests.get(url,timeout=60)
        html = res.text
        font_dict = {}
        y_list = re.findall(r'd="M0 (\d+?) ', html)
        if y_list:
            font_list = re.findall(r'<textPath .*?>(.*?)<', html)
            for i, string in enumerate(font_list):
                y_offset = self.start_y - int(y_list[i])

                sub_font_dict = {}
                for j, font in enumerate(string):
                    x_offset = -j * self.font_size
                    sub_font_dict[x_offset] = font

                font_dict[y_offset] = sub_font_dict

        else:
            font_list = re.findall(r'<text.*?y="(.*?)">(.*?)<', html)

            for y, string in font_list:
                y_offset = self.start_y - int(y)
                sub_font_dict = {}
                for j, font in enumerate(string):
                    x_offset = -j * self.font_size
                    sub_font_dict[x_offset] = font

                font_dict[y_offset] = sub_font_dict
        print('字体字典',font_dict)
        return font_dict

    def _get_font_dict(self, url):
        """
            获取css样式对应文字的字典
        """
        print('解析svg成字典的css', url)
        res = requests.get(url, headers=self._css_headers,cookies=self._cookies,timeout=60)
        html = res.text

        background_image_link = re.findall(r'background-image: url\((.*?)\);', html)
        print('带有svg的链接', background_image_link)
        assert background_image_link
        background_image_link = 'http:' + background_image_link[0]
        html = re.sub(r'span.*?\}', '', html)
        group_offset_list = re.findall(r'\.([a-zA-Z0-9]{5,6}).*?round:(.*?)px (.*?)px;', html)  # css中的类
        print('css中class对应坐标', group_offset_list)
        font_dict_by_offset = self._get_font_dict_by_offset(background_image_link)  # svg得到这里面对应成字典
        print('解析svg成字典', font_dict_by_offset)


        for class_name, x_offset, y_offset in group_offset_list:
            y_offset = y_offset.replace('.0', '')
            x_offset = x_offset.replace('.0', '')
            # print(y_offset,x_offset)
            if font_dict_by_offset.get(int(y_offset)):
                self.font_dict[class_name] = font_dict_by_offset[int(y_offset)][int(x_offset)]

        return self.font_dict

    def _data_pipeline(self, data):
        """
            处理数据
        """
        print('最终数据:',data)

    def _parse_comment_page(self, doc):
        """
            解析评论页并提取数据
        """
        for li in doc.xpath('//*[@class="reviews-items"]/ul/li'):

            name = li.xpath('.//a[@class="name"]/text()')[0].strip('\n\r \t')
            try:
                star = li.xpath('.//span[contains(./@class, "sml-str")]/@class')[0]
                star = re.findall(r'sml-rank-stars sml-str(.*?) star', star)[0]
            except IndexError:
                star = 0
            time = li.xpath('.//span[@class="time"]/text()')[0].strip('\n\r \t')
            pics = []

            if li.xpath('.//*[@class="review-pictures"]/ul/li'):
                for pic in li.xpath('.//*[@class="review-pictures"]/ul/li'):
                    print(pic.xpath('.//a/@href'))
                    pics.append(pic.xpath('.//a/img/@data-big')[0])
            comment = ''.join(li.xpath('.//div[@class="review-words Hide"]/text()')).strip('\n\r \t')
            if not comment:
                comment = ''.join(li.xpath('.//div[@class="review-words"]/text()')).strip('\n\r \t')

            data = {
                'name': name,
                'comment': comment,
                'star': star,
                'pic': pics,
                'time': time,
            }
            self._data_pipeline(data)

    def _get_conment_page(self):  # 获得评论内容
        """
            请求评论页，并将<span></span>样式替换成文字
        """
        while self._cur_request_url:
            self._delay_func()
            print('[{now_time}] {msg}'.format(now_time=datetime.datetime.now(), msg=self._cur_request_url))
            res = requests.get(self._cur_request_url, headers=self._default_headers, cookies=self._cookies)
            html = res.text
            class_set = set()
            for span in re.findall(r'<span class="([a-zA-Z0-9]{5,6})"></span>', html):
                class_set.add(span)
            for class_name in class_set:
                html = re.sub('<span class="%s"></span>' % class_name, self._font_dict[class_name], html)
            doc = etree.HTML(html)
            self._parse_comment_page(doc)
            try:
                self._default_headers['Referer'] = self._cur_request_url
                next_page_url = 'http://www.dianping.com' + doc.xpath('.//a[@class="NextPage"]/@href')[0]
            except IndexError:
                next_page_url = None
            self._cur_request_url = next_page_url

    def run(self):
        self._css_link = self._get_css_link(self._cur_request_url)
        print('css 的连接', self._css_link)
        self._font_dict = self._get_font_dict(self._css_link)
        self._get_conment_page()


if __name__ == "__main__":
    COOKIES = '换上你自己的cookie_lxsdk_cuid=1699b152d90c8-04b0e0-1699b152d91c8; _lxsdk=1699b481697-541f3415-1fa400-152d91c8; _hc.v=992d8c67-a9b0-ee61-c6cf-ed9b42cfe11f.1553085051; ctu=cc29f77c02b4556c6a1db1c67c5c10e084f7f63d00208c59788c11a4845348aa; ua=aJay13; aburl=1; s_ViewType=10; Hm_lvt_e6f449471d3527d58c46e24efb4c343e=1557817381; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1559535631; cy=10; cye=tianjin; uamo=15993248973; dper=af0e70c61c6f98289269ed0f03b97c48a420a5b5ea2e1e33a40ee88662a6acd6a28707ba4a125f2cf0cb043e4d8dc66939c01b24752bfe3aeb807f53c3b411b50117cf5195d1fe2e7db9d1074b85ca4cd0720e1d8f71fc229d3eb6eb5d9df07b; ll=7fd06e815b796be3df069dec7836c3df; _lxsdk_s=16b6c84fcbc-234-e0d-4d4%7C%7C417'
    dp = DianpingComment('412xx21', cookies=COOKIES)
    dp.run()
