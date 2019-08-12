# -*- coding: UTF-8 -*-
__author__ = 'Joynice'

import os
from core.QCWY import QCWY
from core.boss import Boss
from core.zhilian import ZhiLian
from core.lagou import LaGou
from multiprocessing import Pool


# TODO:Boss直聘反爬



if __name__ == '__main__':
    downloadpath = os.path.join(os.getcwd(), 'save-data')
    if os.path.exists(downloadpath):
        city = input('请输入城市名：')
        keyword = input('请输入搜索关键词：')
        if keyword != None and city!=None:
            print('''
            请选择获取的网站如下：
            1. 前程无忧
            2. Boss直聘 
            3. 智联招聘
            4. 拉钩网
            5. 全部
            输入选项前方数字，进行选择！！！
            ''')
            web = input('请输入选项(数字)：')
            if web == '1':
                QCWY(city=city, keyword=keyword).run()
            elif web == '2':
                Boss(city=city, keyword=keyword).run()
            elif web == '3':
                ZhiLian(city=city, keyword=keyword).run()
            elif web == '4':
                LaGou(city=city, keyword=keyword).run()
            elif web == '5':
                pool = Pool(processes=4)
                for i in [ZhiLian(city=city, keyword=keyword).run(), QCWY(city=city, keyword=keyword).run(), Boss(city=city, keyword=keyword).run(), LaGou(city=city, keyword=keyword).run()]:
                    pool.apply_async(i)
                pool.close()
                pool.join()


            print('数据爬取完成，请进入save-data文件夹中取出文件')
    else:
        print('没有找到save-data文件夹！请创建后重新启动！')

