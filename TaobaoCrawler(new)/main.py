# encoding: utf-8

from config import *
import requests
import hashlib
import time
from urllib.parse import quote
import threading


class TaoBao:
    def __init__(self, str_searchContent, num_pageSize, num_page, appKey, threads_num_get_pages, threads_num_get_comments, switch_save, proxies):
        self.str_searchContent = str_searchContent
        self.num_pageSize = num_pageSize
        self.num_page = num_page
        self.appKey = appKey
        self.threads_num_get_pages = threads_num_get_pages
        self.threads_num_get_comments = threads_num_get_comments
        self.switch_save = switch_save
        self.proxies = proxies
        self.cookie = ''
        self.token = ''
        self.file_name = ''
        self.L_itemId = []

        self.run()

    def first_requests(self):
        # 第一次请求,无cookie请求,获取cookie
        base_url = 'https://h5api.m.taobao.com/h5/mtop.alimama.union.sem.landing.pc.items/1.0/?jsv=2.4.0&appKey=12574478&t=1582738149318&sign=fe2cf689bdac8258a1d12507a06bd289&api=mtop.alimama.union.sem.landing.pc.items&v=1.0&AntiCreep=true&dataType=jsonp&type=jsonp&ecode=0&callback=mtopjsonp1&data=%7B%22keyword%22%3A%22%E8%8B%B9%E6%9E%9C%E6%89%8B%E6%9C%BA%22%2C%22ppath%22%3A%22%22%2C%22loc%22%3A%22%22%2C%22minPrice%22%3A%22%22%2C%22maxPrice%22%3A%22%22%2C%22ismall%22%3A%22%22%2C%22ship%22%3A%22%22%2C%22itemAssurance%22%3A%22%22%2C%22exchange7%22%3A%22%22%2C%22custAssurance%22%3A%22%22%2C%22b%22%3A%22%22%2C%22clk1%22%3A%22%22%2C%22pvoff%22%3A%22%22%2C%22pageSize%22%3A%22100%22%2C%22page%22%3A%22%22%2C%22elemtid%22%3A%221%22%2C%22refpid%22%3A%22%22%2C%22pid%22%3A%22430673_1006%22%2C%22featureNames%22%3A%22spGoldMedal%2CdsrDescribe%2CdsrDescribeGap%2CdsrService%2CdsrServiceGap%2CdsrDeliver%2C%20dsrDeliverGap%22%2C%22ac%22%3A%22%22%2C%22wangwangid%22%3A%22%22%2C%22catId%22%3A%22%22%7D'
        try:
            with requests.get(base_url) as response:
                get_cookies = requests.utils.dict_from_cookiejar(
                    response.cookies)
                _m_h5_tk = get_cookies['_m_h5_tk']
                _m_h5_tk_enc = get_cookies['_m_h5_tk_enc']
                self.token = _m_h5_tk.split('_')[0]
                self.cookie = '_m_h5_tk={}; _m_h5_tk_enc={}'.format(
                    _m_h5_tk, _m_h5_tk_enc)
        except Exception as e:
            print('first_requests 出错: ', e)

    def sign(self, token, tme, appKey, data):
        st = token+"&"+tme+"&"+appKey+"&"+data
        m = hashlib.md5(st.encode(encoding='utf-8')).hexdigest()
        return(m)

    def second_requests(self):
        # 第二次带cookie请求,返回数据并存储
        searchContent = '"sc"'.replace('sc', self.str_searchContent)
        pageSize = '"ps"'.replace('ps', str(self.num_pageSize))  # 每页结果属
        page = '"p"'.replace('p', str(self.num_page))  # 第几页

        str_data = '{"keyword":'+searchContent+',"ppath":"","loc":"","minPrice":"","maxPrice":"","ismall":"","ship":"","itemAssurance":"","exchange7":"","custAssurance":"","b":"","clk1":"","pvoff":"","pageSize":'+pageSize+',"page":' + \
            page+',"elemtid":"1","refpid":"","pid":"430673_1006","featureNames":"spGoldMedal,dsrDescribe,dsrDescribeGap,dsrService,dsrServiceGap,dsrDeliver, dsrDeliverGap","ac":"","wangwangid":"","catId":""}'
        data = quote(str_data, 'utf-8')

        tme = str(time.time()).replace('.', '')[0:13]

        sgn = self.sign(self.token, tme, self.appKey, str_data)

        url = 'https://h5api.m.taobao.com/h5/mtop.alimama.union.sem.landing.pc.items/1.0/?jsv=2.4.0&appKey={}&t={}&sign={}&api=mtop.alimama.union.sem.landing.pc.items&v=1.0&AntiCreep=true&dataType=jsonp&type=jsonp&ecode=0&callback=mtopjsonp2&data={}'.format(
            appKey, tme, sgn, data)

        headers = {'cookie': self.cookie}  # 未使用proxies
        try:
            with requests.get(url, headers=headers) as res:
                html = res.text

                res_str = html.split(
                    '"mainItems":')[-1].split('},"ret":')[0].replace('true', '"true"').replace('false', '"false"')
                res_list = eval(res_str)
                if self.switch_save == 0:
                    self.switch_save_0(res_list)
                elif self.switch_save == 1:
                    self.switch_save_1(res_list)
                elif self.switch_save == 2:
                    self.switch_save_2(res_list)
                else:
                    print('config.py 文件中存储部分设置有误!')
        except Exception as e:
            print('second_requests 出错: ', e)

    def switch_save_0(self, res_list):
        from save_csv import save_csv
        csv_file_name = self.file_name+'.csv'
        # 返回该页面所有的 itemId 存入 L_itemId 列表中
        self.L_itemId += save_csv(res_list, csv_file_name)
        print('\n爬取项目数目: ', len(self.L_itemId))

    def switch_save_1(self, res_list):
        from save_mysql import save_mysql
        save_mysql(res_list)

    def switch_save_2(self, res_list):
        from save_mysql_redis import save_mysql_redis
        save_mysql_redis(res_list)

    def get_search_page(self):
        print('搜索页面 线程启动: ', threading.current_thread().name)
        for i in range(1, self.num_page+1):
            self.first_requests()   # 可以在此调整获取cookie的频率
            self.second_requests()
            print('完成第 {} 页爬取\n====================\n'.format(i))

    def get_comments_page(self):
        print('评论页面 线程启动: ', threading.current_thread().name)
        time.sleep(5)
        n = 3  # 三次请求 self.L_itemId 无返回, 则认为所有数据爬取完毕
        while True:
            if n == 0:
                break
            try:
                itemId = self.L_itemId.pop(0)
                self.get_comments(itemId)
                n = 3
            except Exception as e:
                n -= 1
                time.sleep(5)

    def get_comments(self, itemId):
        pass

    def run(self):
        tme = str(time.time()).replace('.', '')[0:13]
        self.file_name = '搜索页面'+'_'+self.str_searchContent+'_' + str(self.num_pageSize)+'_' + str(
            self.num_page)+'_'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(tme[:10]))).replace(' ', '_').replace(':', '_')

        threads = []
        # 一条线程爬取搜索页面
        if self.threads_num_get_pages != 1:
            print('请在 config.py 文件中 设置 threads_num_get_pages = 1')
        thread0 = threading.Thread(target=self.get_search_page, args=())
        threads.append(thread0)

        # 新建线程爬取详情页面
        if self.threads_num_get_comments:
            for i in range(self.threads_num_get_comments):
                thread = threading.Thread(
                    target=self.get_comments_page, args=())
                threads.append(thread)

        # 启动多线程
        for t in threads:
            t.start()

        for t in threads:
            t.join()
            print('关闭线程: ', t.name)

        print('主线程结束！', threading.current_thread().name)


if __name__ == "__main__":
    TaoBao(str_searchContent, num_pageSize, num_page, appKey,
           threads_num_get_pages, threads_num_get_comments, switch_save, proxies)
