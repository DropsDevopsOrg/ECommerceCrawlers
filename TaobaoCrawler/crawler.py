import requests
import time
import json
import re
import os
import threading

from settings import KEYWORD,productdb,simildb,cookiedb
from openpyxl import Workbook
from multiprocessing import Process, JoinableQueue

class Crawler():
    def __init__(self, salenum, threadnum, logMessage, errMessage):
        self.db = productdb
        self.cdb = cookiedb
        self.sdb = simildb
        self.page = None
        self.session = None

        self.data_search_shop_Queue = JoinableQueue()
        self.search_url_Queue = JoinableQueue()
        self.logMessage = logMessage
        self.errMessage = errMessage
        self.salenum = salenum
        self.theadnum = threadnum


    def set_session(self):
        headers = {
            'User-Agent': '"Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",',
            'Cookie': self.get_cookie(),
            'Connection': 'close',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'referer': 'https://www.taobao.com/'}
        import urllib3
        urllib3.disable_warnings()
        s = requests.session()
        s.keep_alice = False
        s.verify = False
        # s.cookies.update(self.get_cookie())
        # s.headers.update(HEADERS)
        s.headers = headers
        self.session = s

    def get_cookie(self):  # 获取不为空的cookie
        while True:
            q = self.cdb.get_cookies(flag=1)
            if q == None:
                self.errMessage.put('正在验证cookie，等待……')
                print('时间等待')
                time.sleep(10)
                continue
            else:
                print('获取cookie')
                # d = {}
                d = ""
                if q:
                    self.user = q['user']
                    cookies = q['cookies']
                    for i in (cookies):
                        name = i['name']
                        value = i['value']
                        str1 = name + '=' + value + '; '
                        d += str1
                    # for cookie in cookies:
                    #     d[cookie.get('name')] = cookie.get('value')
                    # print(d)
                    return d

    def get_page(self, url):
        url = url
        self.set_session()
        # r = self.session.get(url, headers=HEADERS, cookies=self.get_cookie())
        r = self.session.get(url, timeout=(14, 15))
        if r.text.find('亲，小二正忙，滑动一下马上回来') > 0:
            print("cookie需要验证!!!")
            self.errMessage.put('cookie需要验证')
            self.cdb.update_cookie_flag2(self.user)
            self.search_url_Queue.put(url)
            return False
        if r.text.find('请输入') > 0:
            self.errMessage.put('cookie无效登录')
            print("Need Login!!!")
            self.cdb.update_cookie_flag0(self.user)
            self.search_url_Queue.put(url)
            return False
        self.page = r.text
        self.parse()

        time.sleep(4)
        return True

    def parse(self):
        pattern = re.compile(r'g_page_config = ({.*});')
        m = re.search(pattern, self.page)
        if not m:
            print('Cannot fount data in this page.')

            return False
        g_page_config = json.loads(m.group(1))
        auctions = g_page_config.get("mods").get("itemlist").get("data").get("auctions")
        for auction in auctions:
            try:
                simil_url_short = auction.get('i2iTags', {"samestyle": '/'}).get('samestyle', {"url", '/'}).get('url',
                                                                                                                '')
            except Exception as e:
                simil_url_short = ''
            d = {}
            d['keyword'] = self.KEYWORD
            d['t_link'] = 'https:' + auction.get('detail_url', '/')
            d['title'] = auction.get('raw_title')
            d['price'] = auction.get('view_price')
            d['shop_name'] = auction.get('nick')
            d['sales_num'] = auction.get('view_sales', '0').replace('人收货', '').replace('人付款', '')
            d['simil_url_short'] = simil_url_short
            d['flag'] = 0
            print(d.get('keyword'), d.get('title'), d.get('simil_url_short'))
            self.db.insert(d)
            self.logMessage.put(d.get('keyword'), d.get('title'), d.get('simil_url_short'))
            self.data_search_shop_Queue.put(d)

    def run_cry(self):
        while True:
            search_url = self.search_url_Queue.get()  # 获得搜寻数据
            print('【{}实时展示需要-请求-的原商品-链接】', self.search_url_Queue.qsize())
            print('Crawling page {}'.format(search_url))
            flag = self.get_page(url=search_url)
            self.search_url_Queue.task_done()

    def simil_parse(self, similpage, search_data):
        if similpage == False:
            simil_data = dict(
                keyword=self.KEYWORD,
                t_link=search_data.get('t_link'),
                title=search_data.get('title'),
                price=search_data.get('price'),
                shop_name=search_data.get('shop_name'),
                sales_num=search_data.get('sales_num'),
                simil_url='https://s.taobao.com' + str(search_data.get('simil_url_short')) + '&sort=sale-desc',
                # 按照销售量递减
                similars='/',
                simil_title='/',
                simil_good_url='/',
                simil_shopname='/',
                simil_price='/',
                simil_sales_num='/',
            )
            print('无相似数据', simil_data)
            self.sdb.insert(simil_data)
            self.save_data(simil_data)
        else:
            json_tr = re.search('g_page_config = ({.*?});', similpage, re.S).group(1)
            data_list = (json.loads(json_tr))
            similars = data_list.get("mods").get('pager').get('data').get('totalCount')  # 同款数量

            try:
                for item in data_list.get("mods").get("recitem").get("data").get("items"):
                    simil_data = dict(
                        keyword=self.KEYWORD,
                        t_link=search_data.get('t_link'),
                        title=search_data.get('title'),
                        price=search_data.get('price'),
                        shop_name=search_data.get('shop_name'),
                        sales_num=search_data.get('sales_num'),
                        simil_url='https://s.taobao.com' + str(search_data.get('simil_url_short')) + '&sort=sale-desc',
                        # 按照销售量递减
                        similars=similars,
                        simil_title=item.get('raw_title'),
                        simil_good_url='https:' + item.get('detail_url'),
                        simil_shopname=item.get('nick'),
                        simil_price=item.get('view_price'),
                        simil_sales_num=item.get('view_sales').replace('人付款', ''),
                    )
                    print('相似数据', simil_data)
                    self.sdb.insert(simil_data)

                    self.logMessage.put(simil_data.get('keyword'),simil_data.get('title'))
                    self.save_data(simil_data)
            except Exception as e:
                pass

    def simil_run_cry(self):
        while True:
            search_data = self.data_search_shop_Queue.get()

            simil_url_short = search_data.get('simil_url_short')
            sales_num = int(search_data.get('sales_num'))  # 销售数量
            print(simil_url_short)

            # TODO：对于没有链接的做'/' 设定销售数量大于多少不再进行爬取
            if int(sales_num) <= int(self.salenum):  # 舍弃销售量小于设定值的链接
                self.data_search_shop_Queue.task_done()
                continue
            if simil_url_short is '':
                # 调用函数去解析 没有这个相似属性
                similpage = False
                self.simil_parse(similpage, search_data)
                self.data_search_shop_Queue.task_done()
                continue

            simil_url = 'https://s.taobao.com' + str(simil_url_short) + '&sort=sale-desc'  # 按照销售量递减
            print('【{}实时展示要-请求-的相似产品-的数量】', self.data_search_shop_Queue.qsize())
            print('要去请求的相似链接', simil_url)

            self.set_session()
            try:
                r = self.session.get(simil_url, timeout=(14, 15))
            except Exception as e:
                pass
            if r.text.find('亲，小二正忙，滑动一下马上回来') > 0:
                print("相似cookie需要验证!!!")
                self.cdb.update_cookie_flag2(self.user)
                self.data_search_shop_Queue.put(search_data)
                self.data_search_shop_Queue.task_done()
                continue
            elif r.text.find('请输入') > 0:
                print("相似Need Login!!!")
                self.cdb.update_cookie_flag0(self.user)
                self.data_search_shop_Queue.put(search_data)
                continue
            else:
                similpage = r.text
                self.simil_parse(similpage, search_data)

                time.sleep(4)
                self.data_search_shop_Queue.task_done()

    def save_data(self, data):
        simil_item = data
        self.ws.append([
            simil_item.get('keyword', '/'),
            simil_item.get('t_link', '/'),
            simil_item.get('title', '/'),
            simil_item.get('price', '/'),
            simil_item.get('shop_name', '/'),
            simil_item.get('sales_num', '/'),
            simil_item.get('similars', '/'),
            simil_item.get('simil_title', '/'),
            simil_item.get('simil_good_url', '/'),
            simil_item.get('simil_shopname', '/'),
            simil_item.get('simil_price', '/'),
            simil_item.get('simil_sales_num', '/'),
            # simil_item.get('simil_url', '/')  # 同款页面s
        ])

    def save_excel(self):

        save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.KEYWORD + '.xlsx')
        self.wb.save(save_path)

    def run(self, keyword):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["搜索词", "链接", "标题", "价格", "店铺名称", "销量", "同款数", "同款标题", "同款链接", "同款店铺", "同款价格", "同款销量", "找同款链接"])

        self.KEYWORD = keyword
        for i in range(1, 2):
            page = str(i * 44)
            url = 'https://s.taobao.com/search?q=' + self.KEYWORD + '&sort=sale-desc&s=' + page
            print('搜索的初始url', url)
            self.search_url_Queue.put(url)

        Thread_list = []
        for i in range(1):
            Tsearch_page = threading.Thread(target=self.run_cry, args=())
            Thread_list.append(Tsearch_page)
        for i in range(self.theadnum):
            Tsimil_page = threading.Thread(target=self.simil_run_cry, args=())
            Thread_list.append(Tsimil_page)
        for p in Thread_list:
            p.daemon = True
            p.start()
        for all in [self.search_url_Queue, self.data_search_shop_Queue]:
            all.join()
        self.save_excel()
        self.logMessage.put('程序爬取结束')
        print('程序爬取结束')


if __name__ == '__main__':
    import threading
    from multiprocessing import JoinableQueue

    errMessage = JoinableQueue()
    logMessage = JoinableQueue()
    # 配置信息
    from settings import CONFIG

    salenum = CONFIG.get('salenum', 50)
    theadnum = CONFIG.get('theadnum', 1)

    for keyword in KEYWORD:
        c = Crawler(salenum=salenum, threadnum=theadnum, logMessage=logMessage, errMessage=errMessage)

        KEYWORD = keyword.get('keyword')
        c.run(KEYWORD)
