import requests
from requests.exceptions import ConnectionError
from lxml import etree

import time
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
import csv
import pandas as pd
from urllib.parse import quote
import re
from fake_useragent import UserAgent
import random

base_url = 'https://www.toutiao.com/api/search/content/'
timestamp = int(time.time()*1000)

ua = UserAgent(verify_ssl=False)
article_url_list = []
csv_name = pd.read_csv("typhoon_toutiao.csv")

page_urls = ["http://dev.kdlapi.com/testproxy",
             "https://dev.kdlapi.com/testproxy",
             ]

# 隧道服务器
tunnel_host = "tps189.kdlapi.com"
tunnel_port = "15818"

# 隧道用户名密码
tid = "t17888082960619"
password = "gid72p4o"

proxies = {
    "http": "http://%s:%s@%s:%s/" % (tid, password, tunnel_host, tunnel_port),
    "https": "https://%s:%s@%s:%s/" % (tid, password, tunnel_host, tunnel_port)
}

# 防止重复
constract_list = []

# 获取到一个页面内所有的article url


def get_article_urls(name):
    decde = quote(name)
    referer = 'https://www.toutiao.com/search/?keyword='+decde
    for offset in range(0, 120, 20):  # 搜索结果有10个页面，所以只120，有时页面没这么多
        params = {
            'aid': 24,
            'app_name': 'web_search',
            'offset': offset,
            'format': 'json',
            'keyword': name,
            'autoload': 'true',
            'count': 20,
            'en_qc': 1,
            'cur_tab': 1,
            'from': 'search_tab',
            'pd': 'synthesis',
            'timestamp': timestamp
        }
        headers = {
            'cookie': 'tt_webid=6781305717874820616; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6781305717874820616; s_v_web_id=59cfa658a89df645e8a82f1618a81bd0; __tasessionId=g8ptymp5v1579144106433',
            'user-agent': ua.random,
            'x-requested-with': 'XMLHttpRequest',
            'referer': referer,
        }
        html = requests.get(url=base_url, params=params,
                            headers=headers, proxies=proxies)
        result = list(html.json().get('data'))
        for item in result:
            article_url = item.get('article_url')   # 提取每篇文章的url
            if article_url and len(article_url) < 100 and (".mp4" not in article_url) and "toutiao.com" in article_url:
                if '/group/' in article_url:
                    article_url = article_url.replace(
                        '/group/', '/a').replace('http://', 'https://www.')
                article_url_list.append(article_url)
                print(article_url)


def request_AND_storage(name):
    filename = name+".csv"
    try:
        get_article_urls(name)
    except Exception as e:
        print(e)

    browser = webdriver.Chrome()

    time.sleep(2)
    for url in article_url_list:
        print(url)
        try:
            browser.get(url)
            time.sleep(1)
            text_res = browser.find_element_by_xpath(
                '//div[@class="article-box"]')
            print(text_res)
            text_res = text_res.text
            print(text_res)
            with open(filename, 'a', encoding='utf-8') as f:
                writer = csv.writer(f)
                L = [name, text_res]
                writer.writerow(L)
        except:
            continue

    browser.close()


if __name__ == '__main__':
    try:
        request_AND_storage('武汉疫情')
        article_url_list = []
        time.sleep(10)
    except Exception as e:
        print(e)
        article_url_list = []
        time.sleep(1)
        continue

