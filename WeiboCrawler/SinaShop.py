#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/9/25 0025'

"""
# text ='KS美妆坤+关注北京 宣武区个人主页关注104粉丝134微博26简介：人生是花，而爱是花蜜。教育信息：湖南工业职业技术学院香港演藝學院'
#
# import re
#
# pattern ='个人主页关注(\d*)粉丝(\d*)微博(\d*)简介'
# result = re.findall(pattern=pattern,string=text)
# print(result)
import os
import queue
import threading

import requests
from openpyxl import Workbook


class SinaWeibo():
    def __init__(self):
        self.wb = Workbook()
        self.KEYWORD = 'weiboShop'  # 文件名称
        self.ws = self.wb.active
        self.ws.append(["微博昵称", "微博粉丝数量", "微博关注数量", "微博链接", "淘宝链接", "淘宝名称", "售价", "封面连接", "外ID"])

        self.headers = {

        }
        self.userlist_queue = queue.Queue()  # 用户列表队列

    def check_shop(self, V_info_dict, page=1):

        vname = V_info_dict.get('name')
        vdomain = 'https:' + V_info_dict.get('domain')
        vfans = V_info_dict.get('fans')
        vid = V_info_dict.get('id').replace('//weibo.com/', '')
        vfollow = V_info_dict.get('follow')
        vweibo = V_info_dict.get('weibo')
        # print(vid)

        url = 'https://shop.sc.weibo.com/aj/h5/shop/recvlist?shopId=&weiboUid={uid}&page={page}'.format(page=page,
                                                                                                        uid=vid)
        print('请求链接', url)
        req = requests.get(url=url, headers=self.headers)
        # print(req.status_code)
        goodsList = req.json().get('data').get('goodsList')
        if goodsList:
            for good in goodsList:
                out_info = []
                turl = good.get('item_url')
                tname = good.get('name')
                tprice = good.get('price')
                timgUrl = good.get('imgUrl')
                out_iid = good.get('out_iid')
                ttotal = good.get('total')

                out_type = good.get('out_type')
                # print(out_type)
                if out_type == "2":  # 2淘宝 3天猫 0 自身
                    out_info.append(vname)  # 微博昵称
                    out_info.append(vfans)  # 微博粉丝数量
                    out_info.append(vfollow)  # 微博关注数量
                    out_info.append(vdomain)  # 微博链接
                    out_info.append(turl)  # 淘宝链接
                    out_info.append(tname)  # 淘宝名称
                    out_info.append(tprice)  # 售价
                    out_info.append(timgUrl)  # 封面连接
                    out_info.append(out_iid)  # 外ID
                    self.save(out_info=out_info)
                    print('保存')
                    return

            if int(ttotal) // 6 - page >= 0:
                page += 1
                if page > 30:
                    return
                self.check_shop(V_info_dict=V_info_dict, page=page)

    def save(self, out_info):
        self.ws.append(out_info)

    def finalily_done(self):
        print('保存csv')
        save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.KEYWORD + '.xlsx')
        self.wb.save(save_path)

    def do_work(self):
        while True:

            V_info_dict = self.userlist_queue.get()
            print('当前队列容量：', self.userlist_queue.qsize())
            try:
                self.check_shop(V_info_dict=V_info_dict)
            except Exception as e:
                pass
            self.userlist_queue.task_done()

    def run(self):
        with open('products.txt', 'r')as f:
            V_infos = f.read().split('\n')
            for V_info in V_infos:
                V_info_dict = eval(V_info)

                self.userlist_queue.put(V_info_dict)
        print('爬取')
        thread_list = []
        for i in range(50):
            Treq_spi = threading.Thread(target=self.do_work)
            thread_list.append(Treq_spi)
        for t in thread_list:
            t.setDaemon(True)
            t.start()
        for q in [self.userlist_queue]:
            q.join()
        print('结束')

        self.finalily_done()  # 保存csv


if __name__ == '__main__':
    sw = SinaWeibo()
    sw.run()

# check_shop(uid=5884212886)
