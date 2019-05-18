#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/5/5 0005'

"""
import csv
import os
import queue
import re
import threading
import time

import requests
from openpyxl import Workbook
from pyquery import PyQuery as pq


class Yaofang():
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(
            ["证书编号", "经营方式", "企业名称", "企业负责人", "发证机关", "法定代表人", "质量负责人", "注册地址", "仓库地址", "经营范围", "发证日期", "有效截止日期"])

        self.page_queue = queue.Queue()
        self.id_queue = queue.Queue()
        self.detail_date = queue.Queue()

        self.headers = {
            "Host": "219.135.157.143",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://219.135.157.143/gdyj/sjwz/yp/sjwzYpjyxkzList.faces",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "817",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "cookie": "JSESSIONID=JSyHhh2DROPMNqjlzgs5NRejZbvDh0GHkedeBf2UUhjD7uAdlJf7!-745441630",
            "User-Agent":
                "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
        }

    def post_data(self, page_num, detailId):
        data = {
            "sjwzYpjyxkzListForm:total": 56453,
            "sjwzYpjyxkzListForm:row": 10,
            "sjwzYpjyxkzListForm:page": page_num,
            "sjwzYpjyxkzListForm:totalPage": 5646,
            "sjwzYpjyxkzListForm:oldRow": 10,
            "sjwzYpjyxkzListForm:select_id": "",
            "sjwzYpjyxkzListForm:zsbh": "",
            "sjwzYpjyxkzListForm:qymc": "",
            "sjwzYpjyxkzListForm:zcdz": "",
            "sjwzYpjyxkzListForm:fzjg": "",
            "sjwzYpjyxkzListForm:_id14": "",
            "sjwzYpjyxkzListForm:_id16": "",
            "sjwzYpjyxkzListForm:_id18": "",
            "sjwzYpjyxkzListForm:_id20": "",
            "sjwzYpjyxkzListForm:sjwzYpjyxkzBean:inputPage": page_num,
            "sjwzYpjyxkzListForm_SUBMIT": 1,
            "detailId": detailId,
            "sjwzYpjyxkzListForm:_link_hidden_": "",
            "sjwzYpjyxkzListForm:_idcl": "sjwzYpjyxkzListForm:sjwzYpjyxkzBean:_id36",
            "javax.faces.ViewState": "rO0ABXVyABNbTGphdmEubGFuZy5PYmplY3Q7kM5YnxBzKWwCAAB4cAAAAAN0AAhfaWQxODk5OXB0ACMvZ2R5ai9zand6L3lwL3Nqd3pZcGp5eGt6TGlzdC54aHRtbA=="
        }
        return data

    def req_page_data(self):
        while True:
            print('是实展示列表剩余进度', self.page_queue.qsize())
            page_num = self.page_queue.get()
            try:
                print('开始爬取', page_num)
                per_page_data_req = requests.post("http://219.135.157.143/gdyj/sjwz/yp/sjwzYpjyxkzList.faces",
                                                  headers=self.headers, data=self.post_data(page_num, detailId=""))

                d = pq(per_page_data_req.text.replace('<?xml version="1.0" encoding="GBK"?>\n', ''))
                tbody_list = d('tbody tr')
                num = 0
                for i in tbody_list.items():
                    num += 1
                    pattern = "detailId','(.*?)']]"
                    detailId = re.findall(pattern, str(i), re.S)
                    print('页面的id', detailId[0])

                    self.id_queue.put({"detailId": detailId[0], "page": page_num, "per_num": page_num * 10 + num})

            except Exception as e:
                self.page_queue.put(page_num)
                print('请求出错', e)
                self.wb.save(r'广东省食品药品监督管理局.xlsx')
                with open('err_page.txt', 'w+')as f:
                    f.write(str(page_num) + '\n')
            self.page_queue.task_done()

    def _detail_data(self, page, detailId):
        detail_data = {
            "sjwzYpjyxkzListForm:total": 56455,
            "sjwzYpjyxkzListForm:row": 10,
            "sjwzYpjyxkzListForm:page": page,
            "sjwzYpjyxkzListForm:totalPage": 5646,
            "sjwzYpjyxkzListForm:oldRow": 10,
            "sjwzYpjyxkzListForm:select_id": "",
            "sjwzYpjyxkzListForm:zsbh": "",
            "sjwzYpjyxkzListForm:qymc": "",
            "sjwzYpjyxkzListForm:zcdz": "",
            "sjwzYpjyxkzListForm:fzjg": "",
            "sjwzYpjyxkzListForm:_id14": "",
            "sjwzYpjyxkzListForm:_id16": "",
            "sjwzYpjyxkzListForm:_id18": "",
            "sjwzYpjyxkzListForm:_id20": "",
            "sjwzYpjyxkzListForm:sjwzYpjyxkzBean:inputPage": page,
            "sjwzYpjyxkzListForm_SUBMIT": 1,
            "detailId": detailId,
            "sjwzYpjyxkzListForm:_link_hidden_": "",
            "sjwzYpjyxkzListForm:_idcl": "sjwzYpjyxkzListForm:sjwzYpjyxkzBean:5:pzzsLink",
            "javax.faces.ViewState": "rO0ABXVyABNbTGphdmEubGFuZy5PYmplY3Q7kM5YnxBzKWwCAAB4cAAAAAN0AAVfaWQxMnB0ACMvZ2R5ai9zand6L3lwL3Nqd3pZcGp5eGt6TGlzdC54aHRtbA=="
        }
        return detail_data

    def detail_req(self):
        while True:
            print('是实展示详情剩余进度', self.id_queue.qsize())
            id_item = self.id_queue.get()
            per_num = id_item.get('per_num')
            page = id_item.get('page')
            detailId = id_item.get('detailId')

            try:
                detail_data_req = requests.post("http://219.135.157.143/gdyj/sjwz/yp/sjwzYpjyxkzList.faces",
                                                headers=self.headers,
                                                data=self._detail_data(page, detailId))

                html = detail_data_req.text.replace('<?xml version="1.0" encoding="GBK"?>\n', '')
                # print(html)
                d = pq(html)
                table = d('#tb_sjwzBjpPzss_table tr').items()

                per_dict = {}
                for i in table:
                    list = []
                    for j in i.find('td').items():
                        list.append(j.text())
                    if len(list) < 2:
                        continue
                    per_dict[list[0]] = list[1]
                # 数据解析完成
                self.detail_date.put(per_dict)
            except Exception as e:
                print('请求出错')
                self.id_queue.put(id_item)
                with open('err_detail.txt', 'a+')as f:
                    f.write(str(id_item) + '\n')
            self.id_queue.task_done()

    def save(self):
        while True:
            id_item = self.detail_date.get()
            print('输出内容', id_item.get('企业名称'))

            self.ws.append(
                [id_item.get('证书编号', ''), id_item.get('经营方式', ''), id_item.get('企业名称', ''), id_item.get('企业负责人', ''),
                 id_item.get('发证机关', ''), id_item.get('法定代表人', '')
                    , id_item.get('质量负责人', ''), id_item.get('注册地址', ''), id_item.get('仓库地址', ''),
                 id_item.get('经营范围', ''), id_item.get('发证日期', ''), id_item.get('有效截止日期', '')]
            )
            self.detail_date.task_done()

    def run(self):
        for page_num in range(1, 5646):
            self.page_queue.put(page_num)
            print(page_num)

        thread_list = []
        for i in range(10):
            Treq_page = threading.Thread(target=self.req_page_data)
            thread_list.append(Treq_page)

        for i in range(100):
            Tdetail_req = threading.Thread(target=self.detail_req)
            thread_list.append(Tdetail_req)

        for i in range(1):
            Tsave = threading.Thread(target=self.save)
            thread_list.append(Tsave)
        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for q in [self.page_queue, self.id_queue, self.detail_date]:
            q.join()

        print('完成')
        self.wb.save(r'广东省食品药品监督管理局56453.xlsx')


if __name__ == '__main__':
    start_time = time.time()
    yf = Yaofang()
    yf.run()
    print('程序用时', time.time() - start_time)
