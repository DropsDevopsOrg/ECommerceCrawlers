# -*- coding:utf-8 -*-
# 多线程，自动创建文件夹，每个页面单独存储一个文件夹

import os
import queue
import re
import threading
import time

import requests
from bs4 import BeautifulSoup

string = 'https://www.quanjing.com/category/1286521/'
url_queue = queue.Queue()
pipei = re.compile('lowsrc="(.*?)" m=')  #


def get_url(page):
    for i in range(1, page + 1):
        url = string + '{}.html'.format(i)  # 更改网址拼接形式
        url_queue.put(url)
    # print(url_queue.queue)


def spider(url_queue):
    url = url_queue.get()
    floder_count = url[-7:-5]
    if floder_count[0] == '/':
        floder_name = floder_count[1]
    else:
        floder_name = floder_count
    os.mkdir('第{0}页'.format(floder_name))  # mkdir只能创建一级目录，makedirs可以创建多级目录,可能是以参数中的‘/’分级
    html = requests.get(url=url, verify=False).text
    soup = BeautifulSoup(html, 'lxml')
    ul = soup.find_all(attrs={"class": "gallery_list"})
    # print(ul)
    lianjies = re.findall(pipei, str(ul))  # 正则匹配必须是字符串类型
    i = 1
    for lianjie in lianjies:
        # print(lianjie)
        result = requests.get(url=lianjie, verify=False).content
        with open('第{0}页\{1}.jpg'.format(floder_name, i), 'ab') as f:
            f.write(result)
        print('第{0}页第{1}张存储完成'.format(floder_name, i))
        i += 1

    if not url_queue.empty():
        spider(url_queue)


def main():
    queue_list = []
    queue_count = 3
    for i in range(queue_count):
        t = threading.Thread(target=spider, args=(url_queue,))
        queue_list.append(t)
    for t in queue_list:
        t.start()
    for t in queue_list:
        t.join()


if __name__ == '__main__':
    page = int(input("请输入需要爬取的页数:"))
    get_url(page)
    start_time = time.time()
    main()
    print("test3用时：%f" % (time.time() - start_time))
