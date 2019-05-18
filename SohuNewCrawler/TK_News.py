#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/4/15 0015'

"""
# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
from datetime import datetime
import tkinter as tk
import os


from db import MongoArticle,MongoUrl,MongoConfig
from multiprocessing import Process, JoinableQueue

from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox



class MainPage(object):
    def __init__(self, master):
        self.window = master
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 1400
        wh = 650
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小
        self.threadnumVar = tk.IntVar()
        self.timeVar = tk.IntVar()
        self.save_pathVar = tk.StringVar()
        self.logMessage = JoinableQueue()
        self.errMessage = JoinableQueue()
        self.dbconf = MongoConfig()
        self.dburl = MongoUrl()
        self.dbarticle = MongoArticle()
        self.create_page()
        self.show_logs()

        self.asyCraler()



    def asyCraler(self):
        from run_main import NewsClawer
        nc = NewsClawer()
        nc.init_set()
        t = threading.Thread(target=nc.run, args=())
        t.start()
        print('启动主线程')

    def say_export_data(self):
        t = threading.Thread(target=self.export_data, args=())
        t.start()
        print('启动主线程保存数据')
        self.exportDbBtn.config(state=tk.DISABLED)



    def _temp_t(self):
        from  souhu.souhu_new import SouhuSpider
        ss = SouhuSpider()
        self.startBtn.config(text='正在采集')
        while True:
            ss.run(self.logMessage,self.errMessage)
            configs = self.dbconf.select_one()
            sleep_time = configs.get("time", 60)
            print(sleep_time)
            time.sleep(int(sleep_time))
            self.errMessage.put('【周期扫描】：{}秒'.format(sleep_time))


    def create_page(self):
        self.meun()  # 菜单
        self.config()  # 配置
        self.log()  # 日志
        self.error_log()  # 系统日志
        self.img()  # 图片
        # self.loading()  # 进度条

    def img(self):  # 图片
        photo = PhotoImage(file='news.png')
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0, column=2, columnspan=2, rowspan=2, sticky=W + E + N + S, padx=5, pady=5)


    def config(self):  # 配置
        Config = tk.LabelFrame(self.window, text="配置", padx=25, pady=5)  # 水平，垂直方向上的边距均为 10
        Config.place(x=30, y=100)
        tk.Label(Config, text="爬取频率/s:").grid(column=0, row=0, sticky='w', pady=5)  #
        tk.Label(Config, text="爬取线程:").grid(column=0, row=1, sticky='w', pady=5)  # 添加波特率标签
        tk.Label(Config, text="保存路径:").grid(column=0, row=2, sticky='w', pady=5)  # 添加波特率标签
        try:
            configs = self.dbconf.select_one()
            self.threadnum = configs.get('thread')
            self.timenum = configs.get('time')
            self.save_path = configs.get('path')
        except Exception as e:
            self.dbconf.insert({"flag": 1, "time": 60, "thread": 10,"path":"news"})
            self.threadnum = 10
            self.timenum = 60
            self.save_path="默认路径news"
        self.threadnumVar.set(self.threadnum)
        self.timeVar.set(self.timenum)
        self.save_pathVar.set(self.save_path)
        self.threadEntry = tk.Entry(Config, textvariable=self.threadnumVar, width=22)
        self.threadEntry.grid(column=1, row=1, pady=5)

        self.timeEntry = tk.Entry(Config, textvariable=self.timeVar, width=22)
        self.timeEntry.grid(column=1, row=0, pady=5)
        print(self.save_pathVar)
        self.pathEntry = tk.Entry(Config, textvariable=self.save_pathVar, width=22)
        self.pathEntry.grid(column=1, row=2, pady=5)

        self.logoutBtn = tk.Button(Config, text="测试路径", command=self.check_path)
        self.logoutBtn.grid(column=2, row=2, pady=5, ipadx=15, padx=15)

        Config_start = tk.LabelFrame(self.window, text="", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Config_start.place(x=30, y=250)
        tk.Button(Config_start, text="更新配置", command=self.updata_config).grid(column=0, row=0, pady=5, ipadx=20,padx=15)
        self.clearDbBtn = tk.Button(Config_start, text="清空数据库", command=self.clearDB)
        self.clearDbBtn.config(bg='red')
        self.clearDbBtn.grid(column=1, row=1, pady=5, ipadx=15,padx=15)
        self.logoutBtn = tk.Button(Config_start, text="清除缓存", command=self.clear_product)
        self.logoutBtn.grid(column=0, row=1, pady=5, ipadx=15,padx=15)

        self.exportDbBtn = tk.Button(Config_start, text="导出数据", command=self.say_export_data)
        # self.exportDbBtn.config(state=tk.DISABLED)
        self.exportDbBtn.grid(column=2, row=1, pady=5, ipadx=15,padx=15)

        self.startBtn = tk.Button(Config_start, text="开始采集", command=self.start_spider)
        self.startBtn.grid(column=0, row=2, pady=5, ipadx=15)
        # self.stopBtn = tk.Button(Config_start, text="停止采集", command=self.stop_spider)
        # self.stopBtn.grid(column=2, row=2, pady=5, ipadx=15)



    def log(self):  # 日志
        self.logMessage.put('欢迎使用【新闻网采集器器定制版ByAjay13】')
        logInformation = tk.LabelFrame(self.window, text="日志", padx=10, pady=10)  # 水平，垂直方向上的边距均为10
        logInformation.place(x=450, y=100)
        self.logInformation_Window = scrolledtext.ScrolledText(logInformation, width=118, height=22, padx=10, pady=10,
                                                               wrap=tk.WORD)
        self.logInformation_Window.grid()

    def error_log(self):  # 系统日志
        error_logInformation = tk.LabelFrame(self.window, text="系统日志", padx=10, pady=10)  # 水平，垂直方向上的边距均为10
        error_logInformation.place(x=450, y=460)
        self.errorInformation_Window = scrolledtext.ScrolledText(error_logInformation, width=118, height=8, padx=10,
                                                                 pady=10,
                                                                 wrap=tk.WORD)
        self.errorInformation_Window.grid()

    # 菜单说明
    def meun(self):
        menubar = tk.Menu(self.window)
        aboutmemu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='关于', menu=aboutmemu)
        aboutmemu.add_command(label='软件说明', command=self.show_Description)
        aboutmemu.add_command(label='版本', command=self.show_Version)
        aboutmemu.add_command(label='开发者', command=self.show_Developer)
        window.config(menu=menubar)

    # 检测路径
    def check_path(self):
        from  export_article import EexportTxt
        et = EexportTxt()
        path = self.pathEntry.get()
        checkout = et.check_input_path(path)
        if checkout:
            tk.messagebox.showinfo(title='路径', message='路径正确!')
        elif path=="默认路径news":
            tk.messagebox.showinfo(title='路径', message='保存路径将作为默认路径!')
        else:
            tk.messagebox.showerror(title='路径', message='路径不正确!创建正确路径')

    # 导出数据
    def export_data(self):
        from  export_article import EexportTxt
        et = EexportTxt()
        path = self.pathEntry.get()
        et.run(input_path=path,errMessage=self.errMessage)

    # 跟新配置
    def updata_config(self):
        self.logMessage.put('更新配置')
        threadnum = self.threadEntry.get()
        timenum = self.timeEntry.get()
        path = self.pathEntry.get()
        self.dbconf.update(thread=threadnum,time=timenum,path=path)
        tk.messagebox.showinfo(title='配置', message='配置信息更新成功!')



    def start_spider(self):

        # TODO: 获取所有的配置信息函数。
        self.errMessage.put('开始新闻数据采集')

        self.startBtn.config(state=tk.DISABLED)
        t = threading.Thread(target=self._temp_t, args=())
        # t.daemon=True
        t.start()
        print('启动线程')



    def clear_product(self):
        if tk.messagebox.askyesno(title='删除', message='这将清空缓存数据，是否确定删除？'):
            self.errMessage.put('开始清除数据库缓存')
            self.dburl.delete_all({})
            self.errMessage.put('清除数据库缓存结束')
            tk.messagebox.showinfo(title='恭喜', message='清除数据库缓存结束')

    # 清空数据库
    def clearDB(self):
        if tk.messagebox.askyesno(title='删除', message='这将清空所有的数据，是否确定删除？'):
            if tk.messagebox.askyesno(title='再次确认', message='清空数据后请重启软件，是否确定删除？'):
                self.dbconf.delete_all({})
                self.dburl.delete_all({})
                self.dbarticle.delete_all({})

                self.errMessage.put('清除数据库所有数据')
                self.errMessage.put('请重新启动软件，加载配置')
                self.window.update()
                tk.messagebox.showinfo(title='恭喜', message='所有数据清除完成！请重新启动软件，加载配置')

    def log_queue(self):
        while True:
            log = self.logMessage.get()
            date = datetime.now().strftime("%m-%d %H:%M:%S")
            self.logInformation_Window.insert(END, '[{date}][{log}]'.format(date=date, log=log) + '\n')
            self.logInformation_Window.see(END)
            # self.logMessage.task_done()

    def errlog_queue(self):
        while True:
            log = self.errMessage.get()
            if log==1:
                self.exportDbBtn.config(state=tk.ACTIVE)
            date = datetime.now().strftime("%m-%d %H:%M:%S")
            self.errorInformation_Window.insert(END, '[{date}][{log}]'.format(date=date, log=log) + '\n')
            self.errorInformation_Window.see(END)

    def show_logs(self):
        Tlog_queue = threading.Thread(target=self.log_queue, args=())
        Terrlog_queue = threading.Thread(target=self.errlog_queue, args=())
        Tlog_queue.daemon = True
        Tlog_queue.start()
        Terrlog_queue.daemon = True
        Terrlog_queue.start()
        # self.logMessage.join()

    def show_Description(self):
        Description(self.window)

    def show_Version(self):
        Version(self.window)

    def show_Developer(self):
        Developer(self.window)








# 使用说明界面
class Description():
    '''
       软件描述说明介绍界面
       '''

    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.wm_attributes('-topmost', 1)
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 650
        wh = 720
        x = (sw - ww) / 3
        y = (sh - wh) / 3
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小
        self.window.title('使用说明')
        self.create_page()

    def create_page(self):
        Dev = tk.LabelFrame(self.window, text="关于使用说明", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Dev.place(x=50, y=50)
        text = "【使用前仔细阅读使用说明】 \n\n" \
               "使用说明\n" \
               "本项目采用多线程爬取新闻网咨询，爬取速度快，效率高。\n" \
               "根据数据库能做到新闻去重，不去爬取已经爬取过的新闻\n\n" \
               "**注意事项**\n\n" \
               "- 爬取之前检测数据库是否开启成功\n\n" \
               "- 爬取频率：为多久进行一次爬取，默认数值60s，可以根据需求设置\n5分钟=5*60=300秒，时间间隔太小会封ip\n\n" \
               "- 爬取线程： 爬取的线程与电脑的性能有关、一般电脑10个线程，\n电脑性能高可以开50、100个\n\n"\
               "- 爬取的路径：爬取路径错误或者路径不设置将会文件将导出到news文件夹下面\n\n"\
               "- 每次修改配置后，可以需要更新配置，\n\n"\
               "- 清除缓存后，将删除所有的爬取信息\n\n"\
               "- 清空数据库后，将删除所有的的数据库\n\n"\
               "- 建议每隔5天左右清空一次数据库，将减少电脑压力\n\n"\
               "- 关闭程序后结束爬取\n\n"\
               " \n"\
               "- 祝你使用愉快\n"\

        tk.Label(Dev, text=text, justify='left').grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号


# 版本说明界面
class Version():
    '''
    软件版本说明介绍界面
    '''

    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.wm_attributes('-topmost', 1)
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 400
        wh = 300
        x = (sw - ww) / 3
        y = (sh - wh) / 3
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小
        self.window.title('软件版本')
        self.create_page()

    def create_page(self):
        Dev = tk.LabelFrame(self.window, text="关于版本更新", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Dev.place(x=50, y=50)
        text = " 2019年5月 10日 版本：V1.0 正式版\n  " \
               " 2019年5月 09日 版本：V0.2\n "
        tk.Label(Dev, text=text).grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号


# 开发者说明界面
class Developer():
    '''
    软件开发者介绍界面
    '''

    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.wm_attributes('-topmost', 1)
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 400
        wh = 300
        x = (sw - ww) / 3
        y = (sh - wh) / 3
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小
        self.window.title('开发者')
        self.create_page()

    def create_page(self):
        Dev = tk.LabelFrame(self.window, text="关于开发者", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Dev.place(x=50, y=50)
        text = " 作者：AJay13\n" \
               " 技能：熟悉各项爬虫与反爬虫，数据清洗，\n         网站搭建，软件编写\n" \
               " 联系：BoeSKh5446sa23sadKJH84ads5\n"
        tk.Label(Dev, text=text, justify='left').grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号


# 版本测试时间
def test_time(over_time):
    from datetime import datetime
    d2 = datetime.strptime(over_time, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    if d2 > now:
        return True
    else:
        return False


if __name__ == '__main__':

    if test_time('2020-5-11 16:00:00'): # 测试授权日期
        window = tk.Tk()  # 父容器
        print('开始')
        window.title("新闻网采集器器定制版ByAjay13")  # 父容器标题
        basePath = os.path.abspath(os.path.dirname(__file__))
        print('base_path基础路径',basePath)
        if not os.path.exists(os.path.join(basePath, 'temp')):
            os.mkdir(os.path.join(basePath, 'temp'))
        if not os.path.exists(os.path.join(basePath, 'log')):
            os.mkdir(os.path.join(basePath, 'log'))
        mongod = os.path.join(basePath, 'bin', 'mongod.exe')
        dbpath = os.path.join(basePath, 'temp')
        logpath = os.path.join(basePath, 'log', 'mongodb.log')
        #'D:\mongodb\bin\mongod.exe --dbpath D:\mongodb\xianyudb --logpath D:\mongodb\tb_log\MongoDB.log --directoryperdb --serviceName mongodb_tb --install'
        if not os.path.exists(logpath):
            os.system(
                '{} --dbpath {} --logpath {} --directoryperdb --serviceName mongodb --install'.format(mongod, dbpath,
                                                                                                         logpath))
            os.system('net start mongodb')
        else:
            os.system('net start mongodb')

        MainPage(window)

        # 前提配置
        # 配置mongodb为数据服务 初始化配置服务
        '''
        启动服务器服务
        尝试链接数据库，搜寻配置项中db=1.链接不成功
            alert 弹出数据库配置错误，尝试自动初始化，或联系管理员
                1.创建本地mongodb的数据库文件夹
                2.创建本地mongodb的数据库日志的文件夹
                3.使用配置服务的命令
                4.启动服务
                5.数据库配置项中插入db为1
        服务正常启动，tk面板加载配置项

        异步爬虫线程启动，按照每隔10秒读取配置项内容。然后加载到进程中
        关键字为：start == 1 开始加入爬取队列
        '''

        print('监听')
        window.mainloop()
    else:
        window = tk.Tk()  # 父容器
        window.title("新闻网采集器器定制版ByAjay13")  # 父容器标题
        window.wm_attributes('-topmost', 1)
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        ww = 400
        wh = 300
        x = (sw - ww) / 3
        y = (sh - wh) / 3
        window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小
        Dev = tk.LabelFrame(window, text="授权超时", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Dev.place(x=50, y=50)
        text = " 你已经超出授权使用期限\n" \
               " 请联系管理员进行提权\n         \n" \
               " 联系：BoeSKh5446sa23sadKJH84ads5\n"
        tk.Label(Dev, text=text, justify='left').grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号
        window.mainloop()
