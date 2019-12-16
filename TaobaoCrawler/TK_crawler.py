#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/4/15 0015'

"""
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import time
import threading
from datetime import datetime
import tkinter as tk
import os

from settings import configdb,keywordb,userinfodb,cookiedb,productdb,simildb
from multiprocessing import Process, JoinableQueue


from tkinter import *
from tkinter import ttk
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
        self.threadnumVar = tk.StringVar()
        self.salenumVar = tk.StringVar()
        self.logMessage = JoinableQueue()
        self.errMessage = JoinableQueue()
        self.create_page()
        self.show_logs()

    def create_page(self):
        self.meun()  # 菜单
        self.keyword()  # 关键字
        self.config()  # 配置
        self.log()  # 日志
        self.error_log()  # 错误日志
        self.user()  # 用户信息
        self.img()  # 图片
        self.loading()  # 进度条

    def img(self):  # 图片
        photo = PhotoImage(file='taobao.png')
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0, column=2, columnspan=2, rowspan=2, sticky=W + E + N + S, padx=5, pady=5)

    def keyword(self):  # 关键字
        Keyword = tk.LabelFrame(self.window, text="关键字", padx=10, pady=10)  # 水平，垂直方向上的边距均为10
        Keyword.place(x=30, y=100)

        self.keywordListBox = Listbox(Keyword, width=35, height=6, )
        self.keywordListBox.pack(side=LEFT)
        keywordScroBar = Scrollbar(Keyword)
        keywordScroBar.pack(side=RIGHT, fill=Y)

        self.keywordListBox['yscrollcommand'] = keywordScroBar.set
        keywords = keywordb.select({})

        for key in keywords:
            keyword = key.get('keyword')

            self.keywordListBox.insert(END, '关键字：{};'.format(keyword))

            keywordScroBar['command'] = self.keywordListBox.yview

        keywordoption = tk.LabelFrame(self.window, text="", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        keywordoption.place(x=30, y=250)

        tk.Button(keywordoption, text="添加关键字", command=self.add_keyword).grid(column=0, row=1, padx=30, pady=5)
        tk.Button(keywordoption, text="删除关键字", command=self.delete_keyword).grid(column=1, row=1, padx=30, pady=5)

    def user(self):  # 用户信息
        User = tk.LabelFrame(self.window, text="微博用户", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        User.place(x=1070, y=100)
        self.userListBox = Listbox(User, width=35, height=9, )
        self.userListBox.pack(side=LEFT)
        userScroBar = Scrollbar(User)
        userScroBar.pack(side=RIGHT, fill=Y)

        self.userListBox['yscrollcommand'] = userScroBar.set
        userinfos = userinfodb.select({})

        for user in userinfos:
            username = user.get('username')
            pwd = user.get('password')
            self.userListBox.insert(END, '账号：{}  密码：{};'.format(username, pwd))

        userScroBar['command'] = self.userListBox.yview
        # userScrotext = scrolledtext.ScrolledText(User, width=30, height=6, padx=10, pady=10, wrap=tk.WORD)
        # userScrotext.grid(columnspan=2, pady=10)
        Useroption = tk.LabelFrame(self.window, text="", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Useroption.place(x=1070, y=300)
        tk.Button(Useroption, text="添加账号", command=self.add_user).grid(column=0, row=1, padx=35, pady=5)
        tk.Button(Useroption, text="删除账号", command=self.delete_use).grid(column=1, row=1, padx=35, pady=5)

    def config(self):  # 配置
        Config = tk.LabelFrame(self.window, text="配置", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Config.place(x=30, y=330)
        tk.Label(Config, text="线程:").grid(column=0, row=0, sticky='w', pady=5)  #
        tk.Label(Config, text="最低销售量:").grid(column=0, row=1, sticky='w', pady=5)  # 添加波特率标签
        try:
            configs  = configdb.select({})
            self.threadnum = configs.get('threadnum')
            self.salenum = configs.get('salenum')

        except Exception as e:
            configdb.insert({"flag":1,"threadnum":0,"salenum":0})
            self.threadnum = 0
            self.salenum = 0
        self.threadnumVar.set(self.threadnum)
        self.salenumVar.set(self.salenum)
        self.threadEntry = tk.Entry(Config, textvariable=self.threadnumVar, width=28)
        self.threadEntry.grid(column=1, row=0, pady=5)

        self.saleEntry = tk.Entry(Config, textvariable=self.salenumVar, width=28)
        self.saleEntry.grid(column=1, row=1, pady=5)
        Config_start = tk.LabelFrame(self.window, text="", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Config_start.place(x=30, y=450)
        tk.Button(Config_start, text="更新配置", command=self.updata_config).grid(column=0, row=0, pady=5, ipadx=15)
        self.clearDbBtn = tk.Button(Config_start, text="清空数据", command=self.clearDB)
        self.clearDbBtn.config(bg='red')
        self.clearDbBtn.grid(column=1, row=0, pady=5, ipadx=15)
        self.exportDbBtn = tk.Button(Config_start, text="导出数据", command='')
        self.exportDbBtn.config(state=tk.DISABLED)
        self.exportDbBtn.grid(column=2, row=0, pady=5, ipadx=15)
        self.testloginBtn = tk.Button(Config_start, text="测试登录", command=self.testLogin)
        self.testloginBtn.grid(column=0, row=1, pady=5, ipadx=15)
        self.loginBtn = tk.Button(Config_start, text="账户登录", command=self.login)
        self.loginBtn.grid(column=1, row=1, pady=5, ipadx=15)
        self.logoutBtn = tk.Button(Config_start, text="清除登录", command=self.clear_CookieDb)
        self.logoutBtn.grid(column=2, row=1, pady=5, ipadx=15)
        self.listenBtn = tk.Button(Config_start, text="开启监听", command=self.listen_spider)
        self.listenBtn.grid(column=0, row=2, pady=5, ipadx=15)
        self.startBtn = tk.Button(Config_start, text="开始采集", command=self.start_spider)
        self.startBtn.grid(column=1, row=2, pady=5, ipadx=15)
        self.stopBtn = tk.Button(Config_start, text="停止采集", command=self.stop_spider)
        self.stopBtn.grid(column=2, row=2, pady=5, ipadx=15)

    def loading(self):
        # 进度条
        Loading = tk.LabelFrame(self.window, text="进度条", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Loading.place(x=350, y=20)
        canvas = tk.Canvas(Loading, width=665, height=22, bg="white")
        canvas.grid()

    def log(self):  # 日志
        self.logMessage.put('欢迎使用【淘宝同款信息采集器】')
        logInformation = tk.LabelFrame(self.window, text="日志", padx=10, pady=10)  # 水平，垂直方向上的边距均为10
        logInformation.place(x=350, y=100)
        self.logInformation_Window = scrolledtext.ScrolledText(logInformation, width=90, height=22, padx=10, pady=10,
                                                          wrap=tk.WORD)
        self.logInformation_Window.grid()

    def error_log(self):  # 错误日志
        error_logInformation = tk.LabelFrame(self.window, text="错误日志", padx=10, pady=10)  # 水平，垂直方向上的边距均为10
        error_logInformation.place(x=350, y=460)
        self.errorInformation_Window = scrolledtext.ScrolledText(error_logInformation, width=90, height=5, padx=10, pady=10,
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

    # 添加关键字
    def add_keyword(self):
        optionKeyword(self.window, self.keywordListBox)

    # 删除关键字
    def delete_keyword(self):
        if tk.messagebox.askyesno('警告', message='是否删除关键字'):
            try:
                value = self.keywordListBox.get(self.keywordListBox.curselection())
                keyword = re.findall('关键字：(.*?);', value.replace('\n', '').replace(' ', ''), re.S)
                keywordb.delete({"keyword":keyword[0]})
                self.keywordListBox.delete(ACTIVE)
                tk.messagebox.showinfo('成功', message='成功删除关键字：{}'.format(keyword[0]))
            except Exception as e:
                tk.messagebox.showerror('错误', message='请选定指定关键字删除')

    # 添加用户账号
    def add_user(self):
        optionUser(self.window, self.userListBox)

    # 删除用户账号
    def delete_use(self):
        if tk.messagebox.askyesno('警告', message='是否删除用户'):
            try:

                value = self.userListBox.get(self.userListBox.curselection())
                user_pwd = re.findall('账号：(.*?)密码：(.*?);', value.replace('\n', '').replace(' ', ''), re.S)
                userinfodb.delete({"username":user_pwd[0][0]})
                self.userListBox.delete(ACTIVE)
                tk.messagebox.showinfo('成功', message='成功删除用户{}'.format(user_pwd[0][0]))
            except Exception as e:

                tk.messagebox.showerror('错误', message='请选定指定账户删除')

    # 跟新配置
    def updata_config(self):
        self.logMessage.put('更新配置')
        threadnum = self.threadEntry.get()
        salenum = self.saleEntry.get()
        print(threadnum)
        print(salenum)
        configdb.update_theadnum(threadnum)
        configdb.update_salenum(salenum)
        tk.messagebox.showinfo(title='配置', message='配置信息更新成功!')


    def start_spider(self):
        # TODO:开始线程爬取
        self.startBtn.config(state=tk.DISABLED,text='正在采集',bg='coral',)
        self.stopBtn.config(state=tk.NORMAL,text='停止采集',bg='#F5F5F5',)
        # TODO: 获取所有的配置信息函数。

        self.logMessage.put('开始淘宝数据采集')
        self.logMessage.put('最专业的数据采集方式')
        def __crawler():
            from crawler import Crawler

            # 配置信息
            from settings import CONFIG,KEYWORD
            salenum = CONFIG.get('salenum', 50)
            theadnum = CONFIG.get('theadnum', 1)
            c = Crawler(salenum=salenum, threadnum=theadnum, logMessage=self.logMessage, errMessage=self.errMessage)

            for keyword in KEYWORD:
                KEYWORD = keyword.get('keyword')
                c.run(KEYWORD)

        TProcess_crawler = threading.Thread(target=__crawler,
                                           args=())
        TProcess_crawler.daemon = True
        TProcess_crawler.start()
        tk.messagebox.showinfo(title='恭喜', message='开启采集！')

    def stop_spider(self):
        # TODO：按钮恢复
        self.startBtn.config(state=tk.NORMAL, text='开始采集',bg='#F5F5F5')
        self.stopBtn.config(state=tk.DISABLED, text='停止采集',bg='#F5F5F5')
        print('停止or 关闭采集')

    # 清空cookie，退出登录
    def clear_CookieDb(self):
        if tk.messagebox.askyesno(title='删除', message='退出账户登录状态，是否确定删除？'):
            cookiedb.delete_all({})
            self.logMessage.put('退出登录状态')
            tk.messagebox.showinfo(title='恭喜', message='退出登录状态！')
    # 清空数据库
    def clearDB(self):
        if tk.messagebox.askyesno(title='删除', message='这将清空所有的数据，是否确定删除？'):
            if tk.messagebox.askyesno(title='再次确认', message='清空数据后请重启软件，是否确定删除？'):
                configdb.delete_all({})
                keywordb.delete_all({})
                userinfodb.delete_all({})
                cookiedb.delete_all({})
                productdb.delete_all({})
                simildb.delete_all({})
                self.logMessage.put('清除数据库所有数据')
                self.window.update()
                tk.messagebox.showinfo(title='恭喜', message='所有数据清除完成！')
    # 测试登录
    def testLogin(self):
        self.logMessage.put('进行账户测试登录，能脱离异地验证')
        from init_fox import Init_Fox
        def __initFox():
            i = Init_Fox()
            i.init_firefox()

        TProcess_initFox = threading.Thread(target=__initFox, args=())
        TProcess_initFox.daemon = True
        TProcess_initFox.start()
        tk.messagebox.showinfo(title='恭喜', message='正在初始化浏览器，请进行模拟登录！')
        self.errMessage.put('浏览器初始化，进行模拟登录')
        
    # 账户登录
    def login(self):
        self.logMessage.put('正在登录')
        from login import CookieGetter

        login = CookieGetter(self.logMessage, self.errMessage)
        def __login():

            from settings import USERINFO
            for userinfo in USERINFO:
                username = userinfo.get('username')
                password = userinfo.get('password')
                print(username, password)
                login.run(username=username, password=password)

        TProcess_login = threading.Thread(target=__login, args=())
        TProcess_login.daemon = True
        TProcess_login.start()
        tk.messagebox.showinfo(title='恭喜', message='正在登录，请等待登录完成！')
        self.errMessage.put('账户正在登录')
    # 开启监听
    def listen_spider(self):
        self.logMessage.put('开启监听')
        from listen import Tester
        def __l():
            tester = Tester(self.logMessage, self.errMessage)
            tester.run()
        TProcess_listen = threading.Thread(target=__l,args=())
        TProcess_listen.daemon = True
        TProcess_listen.start()
        # TProcess_listen.join()
        print('监听开启')
        self.listenBtn.config(state=tk.DISABLED,bg='#F5F5F5')
        tk.messagebox.showinfo(title='恭喜', message='监听开启！')

    def log_queue(self):
        while True:
            log = self.logMessage.get()
            date = datetime.now().strftime("%m-%d %H:%M:%S")
            self.logInformation_Window.insert(END,'[{date}][{log}]'.format(date=date,log=log)+'\n')
            self.logInformation_Window.see(END)
            # self.logMessage.task_done()

    def errlog_queue(self):
        while True:
            log = self.errMessage.get()
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


# 关键字操作
class optionKeyword(object):
    '''
    关键字添加，修改界面
    '''

    def __init__(self, master, userListBox):
        self.master = master
        self.userListBox = userListBox
        self.window = tk.Toplevel(master)
        self.window.wm_attributes('-topmost', 1)
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 400
        wh = 300
        x = (sw - ww) / 4
        y = (sh - wh) / 4
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小

        self.window.title('关键字')
        self.keyword = tk.StringVar()

        self.create_page()

    def create_page(self):
        User = tk.LabelFrame(self.window, text="关键字", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        User.place(x=50, y=80)
        tk.Label(User, text="关键字:").grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号
        self.keywordEntry = tk.Entry(User, textvariable=self.keyword, width=23)
        self.keywordEntry.grid(column=1, row=0, pady=5)
        tk.Button(User, text="确认添加", command=self.add_keyword).grid(columnspan=2, row=2, pady=5, ipadx=10)

    def add_keyword(self):
        keyword = self.keywordEntry.get()



        if keyword is '':
            tk.messagebox.showerror(title='错误', message='关键字不为空！')
        else:
            rechack_keyword = tk.messagebox.askyesno(title='检查', message='请核对{}信息无误后确认添加'.format(keyword))
            if rechack_keyword:
                if keywordb.select_one({"keyword":keyword}):
                    self.keyword.set('')
                    tk.messagebox.showerror('错误', '此关键字已经存在')
                else:
                    keywordb.insert({"keyword":keyword})
                    self.keyword.set('')

                    self.userListBox.insert(END, '关键字：{};'.format(keyword))  # 关键字添加成功
                    # self.window.destroy()
                    # optionUser(self.master)
                    tk.messagebox.showinfo(title='恭喜', message='关键字添加成功！')
            window.update()

    def delete_user(self, user, pwd):

        pass


# 用户数据操作
class optionUser(object):
    '''
    用户账号添加修改页面界面
    '''

    def __init__(self, master, userListBox):
        self.master = master
        self.userListBox = userListBox
        self.window = tk.Toplevel(master)
        self.window.wm_attributes('-topmost', 1)
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 400
        wh = 300
        x = (sw - ww) / 4
        y = (sh - wh) / 3
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小

        self.window.title('淘宝账户')
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.create_page()

    def create_page(self):
        User = tk.LabelFrame(self.window, text="微博账户", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        User.place(x=50, y=80)
        tk.Label(User, text="账户名:").grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号
        tk.Label(User, text="账户密码:").grid(column=0, row=1, sticky='w', pady=5, padx=5)  # 添加用户密码

        self.userEntry = tk.Entry(User, textvariable=self.username, width=23)
        self.userEntry.grid(column=1, row=0, pady=5)

        self.pwdEntry = tk.Entry(User, textvariable=self.password, width=23)
        self.pwdEntry.grid(column=1, row=1, pady=5)

        tk.Button(User, text="确认添加", command=self.add_user).grid(columnspan=2, row=2, pady=5, ipadx=10)

    def add_user(self):
        username = self.userEntry.get()
        pwd = self.pwdEntry.get()

        if username is '' or pwd is '':
            tk.messagebox.showerror(title='错误', message='账户名或密码不为空！')
        else:
            rechack_useinfo = tk.messagebox.askyesno(title='检查', message='请核对{}信息无误后确认添加'.format(username))
            if rechack_useinfo:
                if userinfodb.select_one({"username":username}):
                    self.username.set('')
                    self.password.set('')
                    tk.messagebox.showerror('错误', '此账户已经存在')
                else:
                    userinfodb.insert({"username":username,"password":pwd})
                    self.username.set('')
                    self.password.set('')
                    self.userListBox.insert(END, '账号：{}  密码：{};'.format(username, pwd))  # 同时增加用户到前端上
                    # self.window.destroy()
                    # optionUser(self.master)
                    tk.messagebox.showinfo(title='恭喜', message='账户添加成功！')
            window.update()

    def delete_user(self, user, pwd):

        pass


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
        ww = 580
        wh = 600
        x = (sw - ww) / 3
        y = (sh - wh) / 3
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小
        self.window.title('使用说明')
        self.create_page()

    def create_page(self):
        Dev = tk.LabelFrame(self.window, text="关于使用说明", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Dev.place(x=50, y=50)
        text = "【使用前仔细阅读使用说明】 \n\n" \
               "本软件用于网络淘宝数据爬取，减少人工采集时间\n\n" \
               "注意事项：\n\n" \
               "    1.爬取的线程建议设置账号的数量0.5倍-3倍之间\n\n" \
               "    2.开启前确定账号密码无误，并账号能再本顺利登陆，不出现异地验证\n\n" \
               "    3.启动前在本地开启代理设置\n\n" \
               "    4.首次使用建议使用“测试登陆”尝试登陆\n\n" \
               "    5.账户登录存在时效性。爬取失败，应该尝试退出上次登录状态，然后重新登录\n\n" \
               "    6.开启动态监听，系统能检测存在安全验证的账户，并绕过验证\n\n" \
               "    7.采集过程中任何停止将导致数据重新采集\n\n" \
               "    8.//采集停止后，可导出数据（功能将在下个版本推出）\n\n" \
               "    8.1采用实时导出数据，一个关键字扫描完成后即可自动导出数据\n\n" \
               "    9.清除全部数据后，请重新启动软件，以便清除缓存\n\n" \
               "软件的实用性将根据客户的使用条件进行更新，优化。请密切及时提交错误\n\n" \


        tk.Label(Dev, text=text,justify='left').grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号


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
        text =  " 2019年4月16日 版本：V2.0\n\n" \
                " 2019年4月13日 版本：V1.3\n\n" \
                " 2019年4月 3日 版本：V1.0\n "
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
        tk.Label(Dev, text=text,justify='left').grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号


# # 创建文件夹
# def mkdir_file(file):
#     folder = os.path.exists(file)
#     if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
#         with open(file, 'w')as f:
#             f.write('')

# 测试时间
def test_time(over_time):
    from datetime import datetime
    d2 = datetime.strptime(over_time, '%Y-%m-%d %H:%M:%S')
    now =datetime.now()
    if d2>now:
        return True
    else:return False

if __name__ == '__main__':
    if test_time('2020-4-17 16:0:0'):
        window = tk.Tk()  # 父容器
        window.title("淘宝同款信息采集器定制版ByAjay13")  # 父容器标题
        MainPage(window)
        window.mainloop()
    else:
        window = tk.Tk()  # 父容器
        window.title("淘宝同款信息采集器定制版ByAjay13")  # 父容器标题
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

