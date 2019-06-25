#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/6/22 0022'

"""
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
        self.file_size=300*1024 # 300k

    def _is_input_path(self,input_path):
        '''
        检查文件路径是否存在，不存在就创造一个，存在后定义self保存路径
        :param input_path: 传入的路径
        :return:  self 保存路径
        '''
        if not os.path.exists(input_path):  # 路径函数
            self.save_path = os.path.join(self.base_path, 'titles')
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
        else:
            self.save_path = input_path
            print('存在自定义路径')
            # self.errMessage.put('【导出文件】自定义路径')

    def _is_less_file_size(self): # 是否存在少于固定文件大小的文件
        for root, dirnames, file_paths in os.walk(self.save_path):
            for file_path in file_paths:
                ds = os.path.getsize(os.path.join(root, file_path))
                if ds < self.file_size:
                    print('小于{}kb'.format(self.file_size), file_path)
                    return os.path.join(root, file_path)

            return False

    def save_size_txt(self,title_set):

        if not self.save_file_name:
            file_name = str(time.time()) + uuid()
            self.save_file_name = os.path.join(self.save_path, file_name + '.txt')
        title_list=[]
        for i in title_set:
            title_list.append(i+'\n')
        while True:
            if self.ds < self.file_size:

                if not title_list:
                    # self.errMessage.put('【导出文件】文件保存结束')
                    # self.errMessage.put(1)
                    print('导出完成')
                    print('没有最新的消息')
                    break
                with open(self.save_file_name, 'a+', encoding='gb18030')as f:
                    f.write(''.join(x for x in title_list[0:100]))
                    del title_list[0:100]

            else:
                print('300k文件写完')
                self.errMessage.put("【导出文件】文件保存{}---{}kb".format(self.save_file_name, self.ds / 1000))
                self.ds = 0
                file_name = str(time.time()) + uuid()
                self.save_file_name = os.path.join(self.save_path, file_name + '.txt')
                with open(self.save_file_name, 'a+', encoding='gb18030')as f:
                    f.write('')
            self.ds = os.path.getsize(self.save_file_name)
            print('正在写入数据大小{}kb'.format(self.ds / 1000))
            # self.errMessage.put("正在写入数据{}---{}kb".format(self.save_file_name, self.ds / 1000))

    def run(self, input_path, title_set,errMessage):

        self.errMessage = errMessage
        self._is_input_path(input_path)  # 输入的路径是否完整，如果不完整就用是否存在路径
        less_file = self._is_less_file_size()
        print('存在小文件', less_file)
        # self.errMessage.put('存在小于300k文件……数据自动继续保存')
        self.save_file_name = less_file
        self.save_size_txt(title_set)
        self.errMessage.put('标题导出完成:{}'.format(less_file))


    def check_input_path(self, input_path):
        if os.path.exists(input_path):
            print('路径正确')
            return True
        else:
            print('路径不存在或者不正确')
            return False

if __name__ == '__main__':
    from queue import Queue
    errorMessage=Queue()
    et = EexportTxt()
    et.check_input_path('F:\cache\新建文件夹') # 检测输入的路径是否正确
    et.run(input_path='F:\cache\新建文件夹',errMessage=errorMessage,title_set={'s','a'})