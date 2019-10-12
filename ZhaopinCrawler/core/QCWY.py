__author__ = 'Joynice'
from utils.utils import get_header, get_time
import requests
import queue
from lxml import etree
import threading
import os
import csv


class QCWY(object):
    '''
    前程无忧
    :param
    传入参数:关键字、城市、线程数
    传出：csv文件
    '''

    def __init__(self, keyword, city='北京', thread=10, path=os.getcwd()):
        self.keyword = keyword
        self.city = city
        self.thread = thread
        self.csv_header = ['职位名称', '详细链接', '公司名称', '工作地点', '薪资', '发布时间', '职位信息', '公司信息']
        self.baseurl = 'https://search.51job.com/list/'
        self.header = get_header()
        self.path = path
        self.pagequeue = queue.Queue()
        self.jobqueue = queue.Queue()

    def _get_city_code(self):
        url = 'https://js.51jobcdn.com/in/js/2016/layer/area_array_c.js'
        req = requests.get(url, headers=self.header).text
        a = req.find(self.city)
        return req[a - 9:a - 3]

    def _get_max_page(self):
        city_code = self._get_city_code()
        url = self.baseurl + '{},000000,0000,00,9,99,{},2,1.html'.format(city_code, self.keyword)
        req = requests.get(url=url, headers=self.header)
        req.encoding = 'gbk'
        html = etree.HTML(req.text)
        max_page = html.xpath('//*[@id="resultList"]/div[2]/div[5]/text()')[2][3:]
        for page in range(1, int(max_page) + 1):
            page_url = self.baseurl + '{},000000,0000,00,9,99,{},2,{}.html'.format(city_code, self.keyword, page)
            self.pagequeue.put(page_url)

    def Spider(self):
        while not self.pagequeue.empty():
            url = self.pagequeue.get()
            print('正在爬取：{}'.format(url))
            req = requests.get(url, headers=get_header())
            req.encoding = 'gbk'
            html = etree.HTML(req.text)
            for i in range(4, 54):

                try:
                    title = html.xpath('//*[@id="resultList"]/div[{}]/p/span/a/@title'.format(i))
                    if title[0] == None:
                        break
                    name = html.xpath('//*[@id="resultList"]/div[{}]/span[1]/a/text()'.format(i))
                    url = html.xpath('//*[@id="resultList"]/div[{}]/p/span/a/@href'.format(i))
                    print(url[0])
                    area = html.xpath('//*[@id="resultList"]/div[{}]/span[2]/text()'.format(i))
                    salery = html.xpath('//*[@id="resultList"]/div[{}]/span[3]/text()'.format(i))
                    time = html.xpath('//*[@id="resultList"]/div[{}]/span[4]/text()'.format(i))
                    req1 = requests.get(url[0], headers=get_header())
                    req1.encoding = 'gb2312'
                    html1 = etree.HTML(req1.text)
                    detail = ''.join(html1.xpath('//*[@class="bmsg job_msg inbox"]//*/text()'))
                    if detail.isspace():
                        detail = ''.join(html1.xpath('//*[@class="bmsg job_msg inbox"]/text()'))
                    print(detail)
                    gongsi = ''.join(html1.xpath('//*[@class="tmsg inbox"]/text()'))
                    if gongsi.isspace():
                        gongsi = ''.join(html1.xpath('//*[@class="tmsg inbox"]//*/text()'))
                    data = {
                        "职位名称": title[0],
                        "详细链接": url[0],
                        "公司名称": name[0],
                        "工作地点": area[0],
                        "薪资": salery[0] if len(salery)!=0 else None,
                        "发布时间": time[0],
                        "职位信息": detail,
                        "公司信息": gongsi
                    }
                    self.jobqueue.put(data)
                except:
                    continue

    def run(self):
        self._get_max_page()
        thread_list = []
        for i in range(self.thread):
            t = threading.Thread(target=self.Spider)
            thread_list.append(t)
        for t in thread_list:
            t.setDaemon(True)
            t.start()
        for t in thread_list:
            t.join()
        if os.path.exists(self.path):
            data_list = []
            self.path = os.path.join(self.path,'save-data')
            while not self.jobqueue.empty():
                data_list.append(self.jobqueue.get())
            with open(os.path.join(self.path, '前途无忧招聘_关键词_{}_城市_{}.csv'.format(self.keyword, self.city)), 'w',
                      newline='', encoding='utf-8-sig') as f:
                f_csv = csv.DictWriter(f, self.csv_header)
                f_csv.writeheader()
                f_csv.writerows(data_list)


if __name__ == '__main__':
    a = QCWY(keyword='java', city='北京').run()