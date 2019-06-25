#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/6/22 0022'

"""

import psutil

from tkinter import messagebox

from time import sleep
import threading

import tkinter as tk
import os

from queue import Queue
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.filedialog import askdirectory


class MainPage(object):
    def __init__(self, master):
        self.window = master
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 400
        wh = 650
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小
        self.domainVar = tk.StringVar()
        self.spidermunVar = tk.IntVar()
        self.threadnumVar = tk.IntVar()
        self.timeVar = tk.IntVar()
        self.save_pathVar = tk.StringVar()

        self.base_path=os.path.abspath(os.path.dirname(__file__))
        self.goon_flag = 0

        self.logMessage = Queue()
        self.config_queue= Queue()
        self.flag_queue = Queue()
        self.url_queue = Queue()



        self.create_page() # 初始化界面
        self.show_logs()  # 初始化日志线程
        self.init_monitor() # 初始化进度条

    def create_page(self):
        self.loading()  # 进度条
        self.config()  # 配置
        self.log()  # 日志
        self.meun()  # 菜单

    def monitor_task(self):
        while True:
            start_url = self.url_queue.get()
            self.url_queue.put(start_url)
            print('进度条时间',self.url_queue.qsize())
            sleep(0.8)
            self.change_schedule(self.url_queue.qsize(),self.spidernum)
            self.url_queue.task_done()

    def change_schedule(self, now_schedule, all_schedule):
        self.canvas.coords(self.fill_rec, (5, 5, 6 + (1- now_schedule / all_schedule) * 325, 25))
        self.window.update()
        self.loadingVar.set(str(round(now_schedule / all_schedule * 100, 2)) + '%')

    def loading(self):
        loadingInformation = tk.LabelFrame(self.window, text="爬取任务进度", padx=10, pady=5)  # 水平，垂直方向上的边距均为10
        loadingInformation.place(x=3, y=20)

        frame = Frame(loadingInformation).grid(row=0, column=0)  # 使用时将框架根据情况选择新的位置
        self.canvas = Canvas(loadingInformation, width=330, height=30, bg="white")
        self.canvas.grid(row=0, column=0)
        self.loadingVar = StringVar()
        # 进度条以及完成程度
        self.out_rec = self.canvas.create_rectangle(5, 5, 325, 25, outline="green", width=1)
        self.fill_rec = self.canvas.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="green")

        tk.Label(loadingInformation, textvariable=self.loadingVar).grid(column=1, row=0, sticky='w', pady=2, padx=2)  #
        self.loadingVar.set(str(00.00) + '%')

    def config(self):
        Config = tk.LabelFrame(self.window, text="配置", padx=25, pady=2)  # 水平，垂直方向上的边距均为 10
        Config.place(x=3, y=100)
        tk.Label(Config, text="解析域名:").grid(column=0, row=0, sticky='w', pady=2)  #
        tk.Label(Config, text="解析次数:").grid(column=0, row=1, sticky='w', pady=2)  #
        tk.Label(Config, text="爬取线程:").grid(column=0, row=2, sticky='w', pady=2)  #
        tk.Label(Config, text="爬取频率/s:").grid(column=0, row=3, sticky='w', pady=2)  # 添加波特率标签
        tk.Label(Config, text="保存路径:").grid(column=0, row=4, sticky='w', pady=2)  # 添加波特率标签

        with open(os.path.join(self.base_path,'config.ini'),'r+')as f :  # 读取配置信息
            config =eval(f.read())
        self.domainVar.set(config.get('domain','https://www.baidu.com/'))
        self.spidermunVar.set(config.get('spidernum',1000))
        self.threadnumVar.set(config.get('threadnum',30))
        self.timeVar.set(config.get('timenum',0))
        self.save_pathVar.set(config.get('path',os.path.join(self.base_path,'title')))         # 自定义配置信息
        self.domainEntry = tk.Entry(Config, textvariable=self.domainVar, width=22)
        self.domainEntry.grid(column=1, row=0, pady=2)
        self.spider_numEntry = tk.Entry(Config, textvariable=self.spidermunVar, width=22)
        self.spider_numEntry.grid(column=1, row=1, pady=2)
        self.threadEntry = tk.Entry(Config, textvariable=self.threadnumVar, width=22)
        self.threadEntry.grid(column=1, row=2, pady=2)
        self.timeEntry = tk.Entry(Config, textvariable=self.timeVar, width=22)
        self.timeEntry.grid(column=1, row=3, pady=2)
        self.pathEntry = tk.Entry(Config, textvariable=self.save_pathVar, width=22)
        self.pathEntry.grid(column=1, row=4, pady=2)
        self.pathBtn = tk.Button(Config, text="选择路径", command=self.check_path)
        self.pathBtn.grid(column=2, row=4, pady=2, ipadx=15, padx=10)
        self.config_queue.put(config)
        Config_start = tk.LabelFrame(self.window, text="操作", padx=10, pady=2)  # 水平，垂直方向上的边距均为 10
        Config_start.place(x=3, y=275)
        tk.Button(Config_start, text="更新配置", command=self.updata_config).grid(column=0, row=0, pady=2, ipadx=40,
                                                              padx=15)
        self.startBtn = tk.Button(Config_start, text="开始采集", command=self.start_spider)

        self.startBtn.grid(column=0, row=1, pady=2, ipadx=40, padx=22)
        self.stopBtn = tk.Button(Config_start, text="暂停采集", command=self.stop_spider)
        self.stopBtn.config(state=tk.DISABLED)
        self.stopBtn.grid(column=1, row=1, pady=2, ipadx=40, padx=22)

    def log(self):  # 日志
        self.logMessage.put('欢迎使用【新闻网采集器器定制版ByAjay13】')
        version_message = "  2019年6月20日 版本：V0.1 \n" \
                          "                  - 支持爬虫暂停，继续  \n" \
                          "                  - 支持进度可视化  \n" \
                          "                  - 支持多线程爬取 "
        self.logMessage.put(version_message)
        logInformation = tk.LabelFrame(self.window, text="日志", padx=10, pady=10)  # 水平，垂直方向上的边距均为10
        logInformation.place(x=3, y=380)
        self.logInformation_Window = scrolledtext.ScrolledText(logInformation, width=47, height=13, padx=10, pady=10,
                                                               wrap=tk.WORD)
        self.logInformation_Window.grid()

        # 菜单说明

    def meun(self):
        menubar = tk.Menu(self.window)
        aboutmemu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='关于', menu=aboutmemu)
        aboutmemu.add_command(label='软件说明', command=self.show_Description)
        aboutmemu.add_command(label='版本', command=self.show_Version)
        aboutmemu.add_command(label='开发者', command=self.show_Developer)
        window.config(menu=menubar)

    def show_Description(self):
        Description(self.window)

    def show_Version(self):
        Version(self.window)

    def show_Developer(self):
        Developer(self.window)

    def check_path(self):
        path_ = askdirectory()
        if path_ is not '':
            self.save_pathVar.set(path_)

    # 更新配置
    def updata_config(self):
        config=dict()
        self.config_queue.queue.clear()
        domain = self.domainEntry.get()
        spidernum= self.spider_numEntry.get()
        threadnum = self.threadEntry.get()
        timenum = self.timeEntry.get()
        path = self.pathEntry.get()
        if domain=='' or spidernum=='' or threadnum=='' or timenum=='' or path=='':
            tk.messagebox.showerror(title='配置', message='配置信息不能为空!')
            self.logMessage.put('配置信息不能为空')
        else:
            config.update({"domain":domain,"spidernum":int(spidernum),"threadnum":int(threadnum),"timenum":int(timenum),"path":path})
            with  open(os.path.join(self.base_path,'config.ini'),'w')as f:
                f.write(str(config))
            self.config_queue.put(config)
            self.logMessage.put('更新配置:[域名]{};[数量]{};[线程]{};[频率]{};[路径]{};'.format(domain,spidernum,threadnum,timenum,path))
            tk.messagebox.showinfo(title='配置', message='配置信息更新成功!')

    def log_queue(self):
        while True:
            log = self.logMessage.get()
            self.logInformation_Window.insert(END, '【{log}】'.format( log=log) + '\n')
            self.logInformation_Window.see(END)


    def show_logs(self):
        Tlog_queue = threading.Thread(target=self.log_queue, args=())
        Tlog_queue.daemon = True
        Tlog_queue.start()

    def start_spider(self):
        config = self.config_queue.get()
        self.spidernum = config.get('spidernum')
        self.config_queue.put(config)
        self.flag_queue.queue.clear()
        self.flag_queue.put(1)
        self.startBtn.config(state=tk.DISABLED,text='正在采集',bg='coral',)
        self.stopBtn.config(state=tk.NORMAL,text='暂停采集',bg='#F5F5F5',)
        from zz_spider import ZZSpider
        zzs = ZZSpider()
        t = threading.Thread(target=zzs.run, args=(config,self.url_queue,self.flag_queue,self.logMessage,self.startBtn,self.stopBtn,tk))# config,url_queue,flag_queue,logMessage
        t.start()
        self.logMessage.put('开始采集')
        print('下发完成')

    def stop_spider(self):
        if self.goon_flag==0:
            self.flag_queue.queue.clear()
            self.flag_queue.put(0)
            self.stopBtn.config(state=tk.NORMAL, text='继续采集', bg='coral', )
            self.startBtn.config(state=tk.DISABLED, text='暂停采集', bg='#F5F5F5', )
            self.goon_flag+=1
            self.logMessage.put('暂停采集')

        else:
            self.flag_queue.queue.clear()
            self.flag_queue.put(1)
            self.stopBtn.config(state=tk.NORMAL, text='暂停采集', bg='#F5F5F5', )
            self.startBtn.config(state=tk.DISABLED, text='正在采集', bg='coral', )
            self.goon_flag-=1
            self.logMessage.put('继续采集')

    # 启动一个线程，记录下url_queue中队列的长度，返回给message信号
    def monitor_thread(self):
        m = threading.Thread(target=self.monitor_task)
        m.setDaemon(True)
        m.start()
        self.url_queue.join()

    def init_monitor(self):
        t = threading.Thread(target=self.monitor_thread )
        t.start()
# 杀死进程
def kill_pro(name):
    for proc in psutil.process_iter():
        # print("pid-%d,name:%s" % (proc.pid, proc.name()))
        if proc.name().find(name) == 0:
            print('杀死进程')
            killcmd = 'taskkill /f /im {}'.format(proc.name())
            os.system(killcmd)
            print(killcmd)


def close_windows():
    if messagebox.askyesno(title='关闭程序', message='是否关闭程序？'):
        window.destroy()
        # 调用杀死进程的方法
        print('调用杀死进程的方法')
        kill_pro(name='tk_zzc')


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
               "本项目采用多线程爬取引导蜘蛛池，爬取速度快，效率高。\n" \
               "**注意事项**\n\n" \
               "- 爬取频率：为多久进行一次爬取，默认数值0s，可以根据需求设置，时间间隔太小会封ip\n\n" \
               "- 爬取线程： 爬取的线程与电脑的性能有关、一般电脑20个线程，\n电脑性能高可以开50、100个\n\n" \
               "- 爬取的路径：爬取路径错误或者路径不设置将会文件将导出到title文件夹下面\n\n" \
               "- 关闭程序后结束爬取\n\n" \
               " \n" \

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
        text = " 2019年6月 20日 版本：V1.0 \n"
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

    # 检测路径


# 版本测试时间
def test_time(over_time):
    from datetime import datetime
    d2 = datetime.strptime(over_time, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    if d2 > now:
        return True
    else:
        return False

def create_config_ini():

    print('base_path基础路径', basePath)
    config_path = os.path.join(basePath, 'config.ini')
    if not os.path.exists(config_path):
        with open(config_path, 'a+')as f:
            f.write(str({'spidernum': '1000', 'timenum': '0', 'path':os.path.join(basePath,'title'), 'threadnum': '30', 'domain': 'https://www.baidu.com/'}))
def create_title_dir():
    if not  os.path.exists(os.path.join(basePath,'title')):
        os.makedirs(os.path.join(basePath,'title'))

if __name__ == '__main__':
    window = tk.Tk()  # 父容器
    print('开始')
    window.title("网站泛域名解析定制版v0.1-ByAjay13")  # 父容器标题
    basePath = os.path.abspath(os.path.dirname(__file__))
    if test_time('2020-5-11 16:00:00'):  # 测试授权日期

        create_config_ini() # 配置文件
        create_title_dir() #配置默认路径
        MainPage(window)
        print('监听')
        window.protocol('WM_DELETE_WINDOW', close_windows)
        window.mainloop()
    else:
        window.wm_attributes('-topmost', 1)
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        ww = 400
        wh = 300
        x = (sw - ww) / 3
        y = (sh - wh) / 3
        window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小
        Dev = tk.LabelFrame(window, text="授权超时", padx=10, pady=2)  # 水平，垂直方向上的边距均为 10
        Dev.place(x=50, y=50)
        text = " 你已经超出授权使用期限\n" \
               " 请联系管理员进行提权\n         \n" \
               " 联系：BoeSKh5446sa23sadKJH84ads5\n"
        tk.Label(Dev, text=text, justify='left').grid(column=0, row=0, sticky='w', pady=2, padx=5)  # 添加用户账号
        window.mainloop()
