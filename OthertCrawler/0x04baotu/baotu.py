# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
import os
import queue
import threading
import time

import requests
from bs4 import BeautifulSoup
from lxml import etree


# 时间装饰器
def usetime(func):
    def inner(*args, **kwargs):
        time_start = time.time()
        func(*args, **kwargs)  # 装饰的函数在此运行
        time_run = time.time() - time_start
        print(func.__name__ + '用时 %.2f 秒' % time_run)

    return inner


class Baotu(object):
    '''
    负责爬虫存储
    TODO:
        目标网络有反爬虫机制，多线程下导致有些目标下载失败
        1.解决多线程下网络错误：增加retry机制
        2.异步进行
    注意点：
    requests.text与requests.context区别

    '''

    def __init__(self, url='https://ibaotu.com/shipin/', thread=1, max_page=250, useragent=None):
        '''

        :param url:
        :param thread: 线程数
        :param max_page: 爬取页数
        :param useragent: 请求useragent
        '''

        self.url = url
        self.thread = thread
        self.page = max_page
        self.useragent = useragent
        self.header = self._get_header()
        self.que = queue.Queue()  # 请求队列
        self.fail = queue.Queue()  # 失败队列

        page = self._get_maxpage()
        if self.page > page:
            self.page = page
        super(Baotu, self).__init__()

    # 如果用户没有设置浏览器类型将使用默认浏览器
    def _get_header(self):
        if not isinstance(self.useragent, str):
            self.useragent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
            return {'User-Agent': self.useragent}

    # 检测当前共有多少分页若用户输入大于当前页面分页则使用当前分页
    def _get_maxpage(self):
        req = requests.get(self.url, headers=self.header, timeout=10, verify=False).text
        html = etree.HTML(req)
        return int(html.xpath("//div[@class='pagelist']/a[8]/text()")[0])  # xpath找到class为pagelist的div标签下第8个a标签下的text文本

    # 获取请求列表
    @usetime
    def request(self):
        for i in range(1, self.page + 1):
            try:
                print(self.url)
                req = requests.get(self.url + '6-0-0-0-0-{}.html'.format(i), headers=self.header, timeout=10,
                                   verify=False)
                print('正在爬取第%d页的数据' % i)
                if req.status_code == 200:
                    bs = BeautifulSoup(req.text)
                    for _, n in zip(bs.find_all('video', src=True), bs.find_all('img', {
                        'class': 'scrollLoading'})):  # bs找到所有video、以及class为scrollLoading的img标签
                        self.que.put(
                            {'url': 'http:' + _['src'], 'name': n['alt']})  # 将每个视频组成字典形式放入队列中，{url:视频url,name:视频的名字)}
            except Exception as e:
                print(e)
                pass
        print('共有{}条视频需要下载！'.format(self.que.qsize()))  # 计算队列的长度及存储多少视频字典

    # 进行下载
    @usetime
    def download(self, path=os.getcwd()):  # 默认下载路径为当前文件夹下
        while not self.que.empty():  # 判断如果队列不为空进行下载
            data = self.que.get()  # 从队列中取出视频字典
            try:
                req = requests.get(url=data['url'], headers=self.header, verify=False)
                if req.status_code == 200:
                    print('-' * 10, data['url'], '-' * 10)
                    if not os.path.exists(path):  # 如果用户设置path不存在，则创建该path
                        os.mkdir(path.strip().rstrip('\\'))
                    with open(os.path.join(path, data['name']), 'wb') as f:
                        f.write(req.content)
                else:
                    # 如果请求失败，等待2秒重新下载，感觉没用，继续完善
                    time.sleep(2)
                    req2 = requests.get(url=data['url'], headers=self.header, verify=False)
                    if req2.status_code == 200:
                        print('+' * 10, data['url'], '+' * 10)
                        with open(os.path.join(path, data['name']), 'wb') as f:
                            f.write(req.content)
                    else:
                        self.fail.put(data)  # 将失败的字典存入fail队列中
                        print(data['name'] + '\t' + '下载失败！')
            except Exception as e:
                print(e)
                continue

    # 控制线程，进行工作
    def run(self):
        t1 = threading.Thread(target=self.request)  # request线程，进行生产者任务
        t1.start()  # 线程启动
        t1.join()  # 等待其他线程结束，再结束线程
        thread_list = []
        for i in range(self.thread):  # 创建多个download线程
            t = threading.Thread(target=self.download, args=('D:\\video',))
            thread_list.append(t)
        for t in thread_list:
            t.start()


if __name__ == '__main__':
    a = Baotu(max_page=10, thread=1).run()
# D:\video
