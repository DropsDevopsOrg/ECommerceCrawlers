#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/4/16 0016'

"""

from cookiepool.settings import TEST_URL

from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from cookiepool.settings import HEADLESS

class Init_Fox():
    def __init__(self):
        self.test_url = TEST_URL
        self.main_url = 'https://s.taobao.com'
        self.url = 'https://s.taobao.com/search?q=袜子&sort=sale-desc&s=88'
        self.loginurl = 'https://login.taobao.com/member/login.jhtml'
    def init_firefox(self):
        self.option = webdriver.FirefoxOptions()
        if HEADLESS:
            self.option.add_argument('--headless')
        self.option.set_preference('network.proxy.type', 1)
        self.option.set_preference('network.proxy.http', '127.0.0.1')  # IP为你的代理服务器地址:如‘127.0.0.0’，字符串类型
        self.option.set_preference('network.proxy.http_port', 8888)
        self.option.set_preference('network.proxy.ssl', '127.0.0.1')
        self.option.set_preference('network.proxy.ssl_port', 8888)
        self.option.set_preference('network.proxy.socks', '127.0.0.1')
        self.option.set_preference('network.proxy.socks_port', 8888)
        self.option.set_preference('network.proxy.ftp', '127.0.0.1')
        self.option.set_preference('network.proxy.ftp_port', 8888)
        self.option.set_preference("permissions.default.image", 2)  # 不加载图片,加快访问速度
        self.browser = webdriver.Firefox(executable_path='geckodriver.exe', options=self.option)
        self.browser.get(self.loginurl)
        self.wait = WebDriverWait(self.browser, 20)  # 超时时长为10
        self.short_wait = WebDriverWait(self.browser, 5)  # 超时时长为10

if __name__ == '__main__':
    i = Init_Fox()
    i.init_firefox()