#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/3/21 0021'

"""
import datetime
import random
import time
import re

# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
from lxml import etree
import requests


class DianpingComment:
    font_size = 14
    start_y = 23

    def __init__(self, shop_id, cookies, delay=7, handle_ban=False):
        self.shop_id = shop_id
        self._delay = delay
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
        if handle_ban:
            print('不想写跳过验证了')
            # self._browser = self._init_browser()
            # self._handle_ban()

    def run(self):
        self._css_link = self._get_css_link(self._cur_request_url)
        self._font_dict = self._get_font_dict(self._css_link)
        self._get_conment_page()

    def _delay_func(self):
        delay_time = random.randint((self._delay - 2) * 10, (self._delay + 2) * 10) * 0.1
        print('睡一会',delay_time)
        time.sleep(delay_time)

    # def _init_browser(self):
    #     """
    #         初始化游览器
    #     """
    #     chrome_options = Options()
    #     chrome_options.add_argument('--headless')
    #     chrome_options.add_argument('--disable-gpu')
    #     browser = webdriver.Chrome(chrome_options=chrome_options)
    #     browser.get(self._cur_request_url)
    #     for name, value in self._cookies.items():
    #         browser.add_cookie({'name': name, 'value': value})
    #     browser.refresh()
    #     return browser

    # def _handle_ban(self):
    #     """
    #         爬取速度过快，出现异常时处理验证
    #     """
    #     try:
    #         self._browser.refresh()
    #         time.sleep(1)
    #         button = self._browser.find_element_by_id('yodaBox')
    #         move_x_offset = self._browser.find_element_by_id('yodaBoxWrapper').size['width']
    #         webdriver.ActionChains(self._browser).drag_and_drop_by_offset(
    #             button, move_x_offset, 0).perform()
    #     except:
    #         pass

    def _format_cookies(self, cookies):
        cookies = {cookie.split('=')[0]: cookie.split('=')[1]
                   for cookie in cookies.replace(' ', '').split(';')}

        return cookies

    def _get_conment_page(self):   # 获得评论内容
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

    def _data_pipeline(self, data):
        """
            处理数据
        """
        print(data)

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
            pics =[]

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
                'pic':pics,
                'time': time,
            }
            self._data_pipeline(data)
    def _get_css_link(self, url):
        """
            请求评论首页，获取css样式文件
        """
        res = requests.get(url, headers=self._default_headers, cookies=self._cookies)
        html = res.text
        # print(html)
        # css_link = re.search(r'<link re.*?css.*?href="(.*?svgtextcss.*?)">', html)
        css_link = re.findall(r'<link rel="stylesheet" type="text/css" href="//s3plus.meituan.net/v1/(.*?)">', html)

        assert css_link
        css_link = 'http://s3plus.meituan.net/v1/' + css_link[0]
        return css_link

    def _get_font_dict(self, url):
        """
            获取css样式对应文字的字典
        """
        res = requests.get(url, headers=self._css_headers)
        html = res.text

        background_image_link = re.findall(r'background-image: url\((.*?)\);', html)
        print('带有svg的链接',background_image_link)
        assert background_image_link
        background_image_link = 'http:' + background_image_link[1]
        html = re.sub(r'span.*?\}', '', html)
        group_offset_list = re.findall(r'\.([a-zA-Z0-9]{5,6}).*?round:(.*?)px (.*?)px;', html)  # css中的类
        print('css中class对应坐标',group_offset_list)
        font_dict_by_offset = self._get_font_dict_by_offset(background_image_link) # svg得到这里面图片对应成字典
        print('解析svg成字典',font_dict_by_offset)

        font_dict = {}

        for class_name, x_offset, y_offset in group_offset_list:
            y_offset = y_offset.replace('.0', '')
            x_offset = x_offset.replace('.0', '')
            # print(y_offset,x_offset)
            if font_dict_by_offset.get(int(y_offset)):
                font_dict[class_name] = font_dict_by_offset[int(y_offset)][int(x_offset)]

        return font_dict

    def _get_font_dict_by_offset(self, url):
        """
            获取坐标偏移的文字字典, 会有最少两种形式的svg文件（目前只遇到两种）
        """
        res = requests.get(url, headers=self._css_headers)
        html = res.text
        font_dict = {}
        # print(html)
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
        return font_dict


if __name__ == "__main__":
    pass



