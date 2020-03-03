import os
import requests
from config import *
from lxml import etree
import csv
# from fake_useragent import UserAgent
import pandas as pd
import threading
import time
import random

# 去重处理
_csv_data = pd.read_csv('./csv/error.csv')
# print(csv_data.duplicated(), len(csv_data))
_csv_data_single = _csv_data.drop_duplicates()
# print(csv_data_single.duplicated(), len(csv_data_single))

_csv_data_single['index'] = range(_csv_data_single.shape[0])
csv_data_res = _csv_data_single.set_index('index')
# print(csv_data_res)

class DealError:
    def __init__(self, cookie, proxies, companies_name, csv_data_res):
        self.cookie = cookie
        self.proxies = proxies
        self.companies_name = companies_name
        # ua = UserAgent(verify_ssl=False)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': self.cookie,
            'DNT': '1',
            'Host': 'www.qichacha.com',
            'Referer': 'https://www.qichacha.com/more_zonecompany.html?id=000c85b2a120712454f4c5b74e4fdfae&p=2',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
            # 'User-Agent': ua.random
        }
        self.path = './csv/'
        self.file_name = self.path+self.companies_name+'.csv'
        self.ListTask = []
        self.csv_data = pd.read_csv('./csv/全国工业园区信息.csv')
        self.csv_data_res = csv_data_res
        self.length = len(self.csv_data_res)

        # print(self.csv_data)
        self.work()

    def get_companies(self, id, page_no):
        url = 'https://www.qichacha.com/more_zonecompany.html?id={}&p={}'.format(
            id, page_no)
        # print(url)
        while True:
            try:
                # with requests.get(url, headers=self.headers, proxies=self.proxies) as response:
                with requests.get(url, headers=self.headers) as response:
                    # response = requests.get(url, headers=self.headers)
                    html = response.text
                    parseHtml = etree.HTML(html)
                    # print(1)

                    return parseHtml
            except Exception as e:
                # log('代理请求故障，重复任务！')
                print('连接故障，重复任务！')
                pass

    def get_companies_all(self, name_thread, id, i, province, city, county, park, area, numcop):
        # i = page_no
        num_writer = 0  # 计算是否有信息写入（反扒机制）
        # for i in range(1, 2):
        parseHtml = self.get_companies(id, i)
        # print(parseHtml)
        # '/firm_2468290f38f4601299b29acdf6eccce9.html'
        rUrls = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/a/@href')
        # '临海市互通汽车销售有限公司'
        rTitle = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/a/text()')
        # '黄剑勇'
        rPerson = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/p[1]/a/text()')
        # '注册资本：1000万元人民币'
        rCapital = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/p[1]/span[1]/text()')
        # '成立日期：2017-09-08'
        rSetTime = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/p[1]/span[2]/text()')
        # '\n              邮箱：3093847569@QQ.COM\n               '
        rEmail = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/p[2]/text()')
        # '电话：0576-85323665'
        rPhone = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/p[2]/span/text()')
        # '\n         地址：浙江省台州市临海市江南街道恒大家居建材城(靖江南路112号)\n       '
        rAddress = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/p[3]/text()')
        # '存续'
        rState = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[3]/span/text()')

        # print(rUrls)
        num_current = len(rUrls)
        for num in range(num_current):
            try:
                url = 'https://www.qichacha.com'+rUrls[num]
                company = rTitle[num]
                person = rPerson[num]
                capital = rCapital[num].replace('注册资本：', '')
                settime = rSetTime[num].replace('成立日期：', '')
                email = rEmail[num].replace(
                    '\n', '').replace('邮箱：', '').strip()
                phone = rPhone[num].replace('电话：', '')
                address = rAddress[num].replace(
                    '\n', '').replace('地址：', '').strip()
                state = rState[num]
                L = [province, city, county, park, area, numcop, company,
                     person, capital, settime, email, phone, address, state, url]
                # print(L)
                with open(self.file_name, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(L)
                    print(L)
                    num_writer += 1
            except Exception as e:
                self.err_log(id, i)
                print('{} 报错 ID: {} , 页码: {}'.format(name_thread, id, i))
        if num_writer == 0:
            print('{} 无信息写入 ID: {} , 页码: {} 请检查反扒机制'.format(name_thread, id, i))
            self.err_log(id, i)
        else:
            print('{} 完成爬取 ID: {} , 页码: {}'.format(name_thread, id, i))

    def err_log(self, id, page):
        err_file = self.path + 'error1.csv'
        if not os.path.exists(err_file):
            header = ['id', 'page']
            with open(err_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
        with open(err_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([id, page])

    def thread_task(self):
        name_thread = threading.current_thread().name
        n = 3  # 三次请求 self.ListTash 无返回, 则认为所有数据爬取完毕
        while True:
            if n == 0:
                break
            try:
                i = self.ListTask.pop(0)
                # print(i)
                id = self.csv_data_res.loc[i, 'id']
                # print(id)
                page_no = self.csv_data_res.loc[i, 'page']

                index = self.get_index(id)  # 原园区所在的索引
                # print(index)
                province = self.csv_data.loc[index, 'province']
                city = self.csv_data.loc[index, 'city']
                county = self.csv_data.loc[index, 'county']
                park = self.csv_data.loc[index, 'park']
                area = self.csv_data.loc[index, 'area']
                numcop = self.csv_data.loc[index, 'numcop']

                self.get_companies_all(name_thread, id, page_no, province,
                                       city, county, park, area, numcop)
                print('\n\n{} 完成爬取 ID: {}, 整体进度: {} / {}\n\n=============================\n'.format(
                    name_thread, id, i+1, self.length))
                n = 3
            except Exception as e:
                n -= 1
                time.sleep(random.randint(3, 10))

    def get_index(self, id):
        url = 'https://www.qichacha.com/zonecompany_'+id
        l_csv_data = len(self.csv_data)
        for index in range(l_csv_data):
            if self.csv_data.loc[index, 'url'] == url:
                return index

    def work(self):
        # 判断\新建文件夹
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            print(self.path+' 文件夹创建成功')

        # 判断\新建文件
        if not os.path.exists(self.file_name):
            header = ['province', 'city', 'county', 'park', 'area', 'numcop', 'company',
                      'person', 'capital', 'settime', 'email', 'phone', 'address', 'state', 'url']
            with open(self.file_name, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)

        for i in range(18200,self.length):
            self.ListTask.append(i)

        threads = []
        for i in range(200):
            thread = threading.Thread(target=self.thread_task, args=())
            threads.append(thread)

        # 启动多线程
        for t in threads:
            t.start()
            print('开启线程: '+t.name)

        for t in threads:
            t.join()
            print('关闭线程: '+t.name)

        print('主线程结束！ '+threading.current_thread().name)


if __name__ == "__main__":
    DealError(cookie, proxies, companies_name, csv_data_res)
