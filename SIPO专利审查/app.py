import os
import time
from PIL import Image
from fateadm_api import TestFunc
import requests
import csv
import pandas as pd
from myui import Ui_Dialog
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

waittime = 100


class MyMainForm(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.TextQThread = TextQthread()
        self.TextQThread.show_in_textBrowser.connect(self.show_in_textBrowser)
        self.pushButton.clicked.connect(self.work)
        self.flag = 1

    def show_in_textBrowser(self, text):
        self.textBrowser.append(text)
        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)

    def work(self):
        if self.flag:
            self.show_in_textBrowser('自动化控制程序 启动成功!!!')
            self.show_in_textBrowser('----------------------\n')
            self.TextQThread.start()
            self.flag = 0


class TextQthread(QThread):
    show_in_textBrowser = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        # self.id = ''
        self.url = 'http://cpquery.cnipa.gov.cn/'
        self.ori_url = ''
        self.shenqingh = ''
        self.browser = ''
        self.data_csv = ''
        self.length = 0

        # self.run()

    def creatfile(self):
        header = ['ID', '查询结果', '专利类型', '申请号/专利号', '发明名称', '申请人', '申请日', '授权公告日', '主分类号', '案件状态',
                  '应缴费用种类', '应缴金额', '应缴截止日', '应缴状态', '已缴费用种类', '已缴金额', '缴费日期', '缴费人姓名', '票据号码(收据号)']
        if not os.path.exists('专利审查结果.csv'):
            with open('专利审查结果.csv', 'a', newline='', encoding='utf8') as f:
                writer = csv.writer(f)
                writer.writerow(header)

    def inputdata(self):
        if not os.path.exists('待查账号.csv'):
            self.show_in_textBrowser.emit(
                '待查账号.csv 文件不存在! 请关闭程序后, 在本文件夹创建本文件!\n')
            return False
        else:
            self.csv_data = pd.read_csv('待查账号.csv')
            _length = len(self.csv_data)
            self.show_in_textBrowser.emit(
                '待查账号.csv 文件含账号个数: {}'.format(_length))
            if _length >= 250:
                self.length = 250
            elif _length == 0:
                return False
            else:
                self.length = _length

            return True

    def searchPage(self, shenqingh):
        self.browser.get(self.ori_url)
        WebDriverWait(self.browser, 600000).until(
            EC.presence_of_element_located((By.ID, 'authImg')))  # 等待验证码已加载出来
        time.sleep(1)
        self.browser.save_screenshot('printscreen.png')
        imgelement = self.browser.find_element_by_id('authImg')  # 定位验证码
        imageopen = Image.open('printscreen.png')
        picwidth = imageopen.width
        scrwidth = self.browser.get_window_size()['width']
        scale = scrwidth / picwidth  # mac 写法, win上有细微差别, win上的我也会写, 但就是不写~~
        # scale = 1
        location = imgelement.location  # 获取验证码 x, y 轴坐标
        size = imgelement.size
        rangle = (int(location['x']/scale), int(location['y']/scale), int(
            (location['x']+size['width'])/scale), int((location['y']+size['height'])/scale))  # 需要截取的坐标

        frame4 = imageopen.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
        frame4 = frame4.convert('RGB')
        frame4.save('code.jpg')  # 保存截图, 打码
        pre = TestFunc()  # 要对此进行判断, 是否识别成功
        # print(pre)
        _shenqingh = self.browser.find_element_by_id('select-key:shenqingh')
        _shenqingh.send_keys(shenqingh)
        _very_code = self.browser.find_element_by_id('very-code')
        _very_code.send_keys(pre)
        time.sleep(0.5)
        _query = self.browser.find_element_by_id('query')
        _query.click()
        os.remove('printscreen.png')
        os.remove('code.jpg')
        # 此处可加循环判断, 是否识别成功, 自己添加吧,我知道怎么写, 但我就是不写~~~

    def dealresult1(self):
        List = []
        WebDriverWait(self.browser, waittime).until(
            EC.presence_of_element_located((By.NAME, 'record:shenqingh')))
        time.sleep(0.5)
        try:
            _record_zhuanlilx = self.browser.find_element_by_xpath(
                '//div[@class="content_boxx"]/table/tbody/tr/td[1]').get_attribute('textContent')
            _record_shenqingh = self.browser.find_element_by_xpath(
                '//div[@class="content_boxx"]/table/tbody/tr/td[2]')
            _record_name = self.browser.find_element_by_xpath(
                '//div[@class="content_boxx"]/table/tbody/tr/td[3]').get_attribute('textContent')
            _record_shenqingrxm = self.browser.find_element_by_xpath(
                '//div[@class="content_boxx"]/table/tbody/tr/td[4]').get_attribute('textContent')
            _record_shenqingr = self.browser.find_element_by_xpath(
                '//div[@class="content_boxx"]/table/tbody/tr/td[5]').get_attribute('textContent')
            _record_shouquanggr = self.browser.find_element_by_xpath(
                '//div[@class="content_boxx"]/table/tbody/tr/td[6]').get_attribute('textContent')
            _record_zhufenlh = self.browser.find_element_by_xpath(
                '//div[@class="content_boxx"]/table/tbody/tr/td[7]').get_attribute('textContent')
            zhuanlilx = _record_zhuanlilx.strip()
            shenqingh = _record_shenqingh.get_attribute('textContent').strip()
            name = _record_name.strip()
            shenqingrxm = _record_shenqingrxm.strip()
            shenqingr = _record_shenqingr.strip()
            shouquanggr = _record_shouquanggr.strip()
            zhufenlh = _record_zhufenlh.strip()
            List = [self.shenqingh, '有', zhuanlilx, shenqingh, name, shenqingrxm,
                    shenqingr, shouquanggr, zhufenlh]
            try:
                _record_shenqingh.click()
            except Exception as e:
                pass
            finally:
                return List
        except Exception as e:
            return [self.shenqingh, '无', ]

    def dealresult2(self, List):
        WebDriverWait(self.browser, waittime).until(
            EC.presence_of_element_located((By.NAME, 'record_zlx:anjianywzt')))
        time.sleep(0.5)
        try:
            anjianywzt = self.browser.find_element_by_name(
                'record_zlx:anjianywzt').get_attribute('title')
            List.append(anjianywzt)
        except Exception as e:
            List.append('')
        finally:
            self.browser.find_element_by_xpath(
                '//div[@class="tab_list"]/ul/li[3]').click()
            return List

    def dealresult3(self, List):
        WebDriverWait(self.browser, waittime).until(
            EC.presence_of_element_located((By.NAME, 'record_yingjiaof:yingjiaofydm')))
        time.sleep(0.5)
        try:
            yingjiaofydm = self.browser.find_element_by_name(
                'record_yingjiaof:yingjiaofydm').get_attribute('title')
            shijiyjje = self.browser.find_element_by_name(
                'record_yingjiaof:shijiyjje').get_attribute('title')
            jiaofeijzr = self.browser.find_element_by_name(
                'record_yingjiaof:jiaofeijzr').get_attribute('title')
            feiyongzt = self.browser.find_element_by_name(
                'record_yingjiaof:feiyongzt').get_attribute('title')
            L1 = [yingjiaofydm, shijiyjje, jiaofeijzr, feiyongzt]
        except Exception as e:
            L1 = ['', '', '', '']
        finally:
            List += L1
        # 此处部分结果无返回,会卡住, 我知道怎么写, 我就是不写~~
        try:
            feiyongzldm = self.browser.find_element_by_name(
                'record_yijiaof:feiyongzldm').get_attribute('title')
            jiaofeije = self.browser.find_element_by_name(
                'record_yijiaof:jiaofeije').get_attribute('title')
            jiaofeisj = self.browser.find_element_by_name(
                'record_yijiaof:jiaofeisj').get_attribute('title')
            jiaofeirxm = self.browser.find_element_by_name(
                'record_yijiaof:jiaofeirxm').get_attribute('title')
            shoujuh = self.browser.find_element_by_name(
                'record_yijiaof:shoujuh').get_attribute('title')
            L2 = [feiyongzldm, jiaofeije, jiaofeisj, jiaofeirxm, shoujuh]
        except Exception as e:
            L2 = ['', '', '', '', '']
        finally:
            List += L2
            return List

    def writecsv(self, List):
        with open('专利审查结果.csv', 'a', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow(List)

    def run(self):
        flg = self.inputdata()
        if flg:
            self.creatfile()
            self.show_in_textBrowser.emit('专利审查结果.csv 文件创建成功/已经存在')
            self.show_in_textBrowser.emit('----------------------\n')
            self.show_in_textBrowser.emit(
                '请在自动启动的 Firefox 浏览器中\n登录 并 点击到查询界面\n然后, 交给自动控制程序!!!')
            self.show_in_textBrowser.emit('======================\n')

            # 启动 \ 登陆
            self.browser = webdriver.Firefox()
            self.browser.get(self.url)

            # 到达搜索页面, 开始制动操作
            WebDriverWait(self.browser, 600000).until(
                EC.presence_of_element_located((By.ID, 'authImg')))  # 等待验证码已加载出来
            # time.sleep(0.5)
            self.ori_url = self.browser.current_url
            # self.id = self.ori_url.split('flowno=')[-1]
            # self.show_in_textBrowser.emit('您登录的 时间戳 为: {}'.format(self.id))
            self.show_in_textBrowser.emit('======================\n')
            self.show_in_textBrowser.emit('开始自动查询(每个账号每次限制查询 250 次):\n')
            for i in range(self.length):
                self.shenqingh = self.csv_data.loc[i, 'ID'].replace(
                    'CN', '').replace('.', '')
                # self.shenqingh = '2014102567666'
                self.searchPage(self.shenqingh)
                List = self.dealresult1()
                # print(List)
                if len(List) == 2:
                    self.writecsv(List)
                    self.show_in_textBrowser.emit(
                        '{}/{}\tID: {}\t未检索到'.format(i+1, self.length, self.shenqingh))
                    self.browser.get(self.ori_url)
                else:
                    List = self.dealresult2(List)
                    # print(List)
                    List = self.dealresult3(List)
                    # print(List)
                    self.writecsv(List)
                    self.show_in_textBrowser.emit(
                        '{}/{}\tID: {}\t写入成功'.format(i+1, self.length, self.shenqingh))
                    self.browser.get(self.ori_url)
            self.browser.get(self.url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.resize(650, 781)
    myWin.setFixedSize(650, 781)

    myWin.show()
    sys.exit(app.exec_())
