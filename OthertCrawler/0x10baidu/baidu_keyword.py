# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
import requests
from lxml import etree
import re
import csv
from datetime import datetime
import queue
import threading
import os
import sys


class BaiduKeyword(object):
    def __init__(self, thread=20, filename=None, number=1000):
        self.baseUrl = 'http://www.baidu.com/s'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        self.csv_header = ['keyword', 'number', 'time']
        self.keyword_queue = queue.Queue()
        self.thread = thread
        self.filename = filename
        self.judge_number = number
        self.basepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '彩票关键词爬取结果')
        if not os.path.exists(self.basepath):
            os.mkdir(self.basepath)
        print(self.thread)

    def Spider(self):
        while not self.keyword_queue.empty():
            keyword = self.keyword_queue.get()
            data = {'wd': keyword}
            try:
                r = requests.get(url=self.baseUrl, params=data, headers=self.headers)
                if r.status_code == 200:
                    html = etree.HTML(r.text)
                    text = html.xpath('//*[@id="container"]/div[2]/div/div[2]/span/text()')
                    number = re.findall('百度为您找到相关结果约(.*?)个', text[0], re.I)[0]
                    if ',' in number:
                        number = int(re.sub(',', '', number))
                else:
                    number = 0
                    print('fail', '-' * 10, keyword)
                row = {'keyword': keyword, 'number': number, 'time': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}
                print('正在扫描{}文件，不要打开该csv文件！'.format(os.path.split(self.path)[1]) + '---' + str(row))
            except Exception as e:
                number = 0
                row = {'keyword': keyword, 'number': number, 'time': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}
            try:
                if int(number) <= self.judge_number:
                    with open(os.path.join(self.basepath, '{}小于{}.csv'.format(self.filename, self.judge_number)), 'a+',
                              newline='') as f:
                        f_csv = csv.DictWriter(f, self.csv_header)
                        f_csv.writerow(row)
                else:
                    with open(os.path.join(self.basepath, '{}大于{}.csv'.format(self.filename, self.judge_number)), 'a+',
                              newline='') as f:
                        f_csv = csv.DictWriter(f, self.csv_header)
                        f_csv.writerow(row)
            except Exception as e:
                with open('fail2.txt', 'a+') as f:
                    f.write(keyword + '\n')

    def run(self, path):
        self.path = path
        with open(path, 'r', encoding='gb18030') as f:
            a = f.readlines()
            for i in a:
                self.keyword_queue.put(i.strip())
            thread_list = []
            for i in range(self.thread):
                t = threading.Thread(target=self.Spider)
                thread_list.append(t)
            for t in thread_list:
                t.setDaemon(True)
                t.start()
            for t in thread_list:
                t.join()


if __name__ == '__main__':
    print('*' * 30)
    print("1. 请爬取的文件(.txt)放到'彩票关键词'目录中进行爬取")
    print("2. 爬取结果存放在'彩票关键词爬取结果'中,保存格式为CSV,其中包含关键字，收录次数，爬取时间'")
    print("3. 不要对程序自带的两个文件夹重命名！！！")
    print("4. 爬取过程中，不要打开正在扫描的csv文件！！！")
    print('*' * 30)
    print("开始进行爬虫设置！！！")
    try:
        thread_num = int(input("请设置线程数（默认线程为20，建议使用20，防止百度封堵）：") or 20)
        judeg_num = int(input("请设置阈值对收录次数进行划分，默认值为1000：") or 1000)
    except:
        print("请输入大于0的整数！！！")
        sys.exit(0)
    if not isinstance(thread_num, int) and not isinstance(judeg_num, int):
        print("参数设置错误，请输入整数！")
        sys.exit(0)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '彩票关键词')
    if os.path.exists(path):
        dirs = os.listdir(path)
        if len(dirs) == 0:
            print("文件夹中没有扫描文件，请将文件放入文件夹后进行扫描！")
            sys.exit(0)
        for txt in dirs:
            key_path = os.path.join(path, txt)
            print('*' * 10 + '开始爬取' + '*' * 10)
            print('-' * 10 + '正在爬取{}文件内容'.format(txt) + '-' * 10)
            BaiduKeyword(filename=txt, thread=thread_num, number=judeg_num).run(key_path)
            os.remove(key_path)
        print('已完成爬取，请提取文件夹中的文件。')
    else:
        print("没有找到'彩票关键词'文件夹，请创建文件夹！")
