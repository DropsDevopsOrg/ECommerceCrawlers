# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
import requests
import csv
import queue


class XiaoMiShop():

    def __init__(self, category):
        self.base_url = 'http://app.mi.com/categotyAllListApi'
        self.base_download = 'http://app.mi.com/download/'
        self.header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        self.csv_header = ['ID', '应用名称', '下载链接']
        self.max_page = 70
        self.category = category
        self.queue = queue.Queue()

    def clean_data(self, data):
        '''
        提取数据，放入队列中
        :param data:
        :return:
        '''
        for i in data:
            app = {}
            app['ID'] = i.get('appId')
            app['应用名称'] = i.get('displayName')
            app['下载链接'] = self.base_download + str(i.get('appId'))
            self.queue.put(app)

    def request(self, page):
        parame = {
            'page': page,
            'categoryId': int(self.category),
            'pageSize': 30
        }
        req = requests.get(url=self.base_url, params=parame)
        req.encoding = req.apparent_encoding
        return req

    def spider_by_page(self, page, retry=3):
        '''
        失败页数重新爬取
        :param page: 失败页数
        :param retry: 重试次数
        :return:
        '''
        if retry > 0:
            print('重试第{}页'.format(page))
            req = self.request(page=page)
            try:
                data = req.json()['data']
                if data:
                    self.clean_data(data)
                    print('第{}页重试成功'.format(page))
            except:
                self.spider_by_page(page=page, retry=retry - 1)

    def spider(self):
        '''
        :param category: 模块id，如游戏：15
        :return:
        '''
        fail_page = []
        for _ in range(self.max_page):
            print('正在爬取第{}页'.format(_))
            req = self.request(_)
            try:
                data = req.json()['data']
            except:
                data = []
                fail_page.append(_)
            if data:
                self.clean_data(data)
            else:
                continue
        if fail_page:
            print('出错的页数：', fail_page)
            for _ in fail_page:
                self.spider_by_page(page=_)
        else:
            print('没有出错')

    def run(self):
        self.spider()
        data_list = []
        while not self.queue.empty():
            data_list.append(self.queue.get())
        with open('{}.csv'.format(self.category), 'w', newline='', encoding='utf-8-sig') as f:
            f_csv = csv.DictWriter(f, self.csv_header)
            f_csv.writeheader()
            f_csv.writerows(data_list)
        print('文件保存成功,打开{}.csv查看'.format(self.category))


if __name__ == '__main__':
    a = XiaoMiShop(15).run()
