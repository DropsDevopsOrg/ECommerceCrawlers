import requests
import time
import json
import re
from dbsimil import Mongo
from dbcookie import DbClient
from settings import KEYWORD, HEADERS


class Crawler():
    def __init__(self):
        self.db = Mongo()
        self.cdb = DbClient()
        self.page = None
        self.session = None
        self.set_session()
        self.search_url_Queue = JoinableQueue()

    def set_session(self):
        s = requests.session()
        s.cookies.update(self.get_cookie())
        s.headers.update(HEADERS)
        self.session = s

    def get_cookie(self): # 获取不为空的cookie
        while True:
            q = self.cdb.get_cookies(flag=1)
            if q==None:
                print('时间等待')
                time.sleep(10)
                continue
            else:
                d = {}
                if q:
                    self.user = q['user']
                    cookies = q['cookies']
                    for cookie in cookies:
                        d[cookie.get('name')] = cookie.get('value')
                    return d


    def get_page(self, url):
        url =url
        #r = self.session.get(url, headers=HEADERS, cookies=self.get_cookie())
        r = self.session.get(url,timeout=(10, 15))
        if r.text.find('亲，小二正忙，滑动一下马上回来') > 0:
            print("cookie需要验证!!!")
            self.cdb.update_cookie_flag2(self.user)
            return False
        if r.text.find('请输入') > 0:
            print("Need Login!!!")
            self.cdb.update_cookie_flag0(self.user)
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
            with open('log_page.txt', 'w') as f:
                f.write(self.page)
            return False
        g_page_config = json.loads(m.group(1))
        auctions = g_page_config['mods']['itemlist']['data']['auctions']
        for auction in auctions:
            try:
                simil_url_short = auction.get('i2iTags', {"samestyle": '/'}).get('samestyle', {"url", '/'}).get('url', '')
            except Exception as e:
                simil_url_short = ''
            d = {}
            d['keyword'] = KEYWORD
            d['t_link'] = 'https:'+auction.get('detail_url','/')
            d['title'] = auction.get('raw_title')
            d['price'] = auction.get('view_price')
            d['shop_name'] = auction.get('nick')
            d['sales_num'] = auction.get('view_sales','0').replace('人收货', '').replace('人付款','')
            d['simil_url_short'] = simil_url_short
            d['flag'] = 0
            print(d.get('keyword'), d.get('title'),d.get('simil_url_short'))
            self.db.insert(d)

    def run_cry(self):
        while True:
            print('【{}实时展示需要-请求-的原商品-链接】', self.search_url_Queue.qsize())

            search_url = self.search_url_Queue.get()  # 获得搜寻数据
            print('Crawling page {}'.format(search_url))
            flag = self.get_page(url=search_url)
            self.search_url_Queue.task_done()

    def run(self):
        for i in range(1, 4):
            page = str(i * 44)
            url = 'https://s.taobao.com/search?q=' + KEYWORD + '&sort=sale-desc&s=' + page
            print('搜索的初始url', url)

            self.search_url_Queue.put(url)

            Thread_list = []
            for i in range(1):
                Tsearch_page = threading.Thread(target=self.run_cry, args=())
                Thread_list.append(Tsearch_page)

            for p in Thread_list:
                p.daemon = True
                p.start()

            for all in [self.search_url_Queue, self.parse_data_search_shop_Queue, self.data_search_shop_Queue,
                        self.parse_data_simil_shop_Queue, self.data_simil_shop_Queue,
                        ]:
                all.join()




if __name__ == '__main__':
    import threading
    from multiprocessing import JoinableQueue
    Crawler().run()
