#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/5/9 0009'

"""


from db import MongoArticle,MongoUrl
mu = MongoUrl()
ma = MongoArticle()




import time
from shortuuid import uuid
import os
#TODO:按照随机的文件名，导出每天的新闻到对应当天时间的文件夹中
'''
输入一个路径、如果路径存在、则使用路径、如果路径不存在则使用文件的路径。输出文件路径所在的位置
导出当天的新闻
'''



class EexportTxt():
    def __init__(self):
        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.ds=0
        self.length_p=30
        self.file_size=300*1024# 300k

    def _is_input_path(self,input_path):
        if not os.path.exists(input_path):  # 路径函数
            self.save_path = os.path.join(self.base_path, 'news')
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
        else:
            self.save_path = input_path
            print('存在自定义路径')
            self.errMessage.put('【导出文件】存在自定义路径')

    def _is_less_file_size(self):
        for root, dirnames, file_paths in os.walk(self.save_path):
            for file_path in file_paths:
                ds = os.path.getsize(os.path.join(root, file_path))
                if ds < self.file_size:
                    print('小于300kb', file_path)
                    return os.path.join(root, file_path)

            return False
    def save_size_txt(self):

        if not self.save_file_name:
            file_name = str(time.time()) + uuid()
            self.save_file_name = os.path.join(self.save_path, file_name + '.txt')
        while True:
            if self.ds < self.file_size:
                article = ma.select_one_update()          # 导出数据库信息的方式
                if not article:
                    self.errMessage.put('【导出文件】文件保存结束')
                    self.errMessage.put(1)
                    print('新闻导出完成')
                    print('没有最新的消息')
                    break
                p = article.get('article')

                leng_p_list =p.split('\n')
                with open(self.save_file_name, 'a+', encoding='utf-8')as f:
                    for leng_p in leng_p_list:
                        if len(leng_p)>=self.length_p:
                            f.write(leng_p)
                            f.write('\n')
            else:
                print('300k文件写完')
                self.errMessage.put("【导出文件】文件保存{}kb".format(self.ds/1000))
                self.ds = 0
                file_name = str(time.time()) + uuid()
                self.save_file_name=os.path.join(self.save_path, file_name + '.txt')
                with open(self.save_file_name, 'a+', encoding='utf-8')as f:
                    f.write('')
            self.ds = os.path.getsize(self.save_file_name)
            print('正在写入数据大小{}kb'.format( self.ds/1000))

    def run(self,input_path,errMessage):
        self.errMessage=errMessage
        self._is_input_path(input_path) # 输入的路径是否完整，如果不完整就用是否存在路径
        less_file = self._is_less_file_size()
        print('存在小文件',less_file)
        self.errMessage.put('存在小文件……数据自动继续保存')
        self.save_file_name=less_file
        self.save_size_txt()

    def check_input_path(self,input_path):
        if os.path.exists(input_path):
            print('路径正确')
            return True
        else:
            print('路径不正确或者不存在')
            return False


if __name__ == '__main__':
    et = EexportTxt()
    et.check_input_path('asd')
    et.run(input_path='asd')





