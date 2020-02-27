from fake_useragent import UserAgent
import requests
from time import sleep
import datetime
from model import WeiboInfo, WeiboTask, engine
from sqlalchemy.orm import sessionmaker

from pyquery import PyQuery as pq
import random

Session = sessionmaker(bind=engine)
session = Session()
ua = UserAgent(verify_ssl=False)



cookies = ""
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Language': 'zh-cn',
    'Cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}


import queue
import threading

class Weibo():
    def __init__(self):
        self.urlqueue = queue.Queue()
        self.sec_urlqueue = queue.Queue()
        self.canshu_queue = queue.Queue()
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_data(self,url):
        sleep(1.5)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': cookies,
            'User-Agent': ua.random}
        # , proxies = proxy
        print(url)
        data = requests.get(url, headers=headers).text
        # print(data)
        return data

    def parse_html(self,pl_feedlist_index, begintime,pageurl):
        canshu_list=[]
        for i in pl_feedlist_index.find('.card-wrap').items():
            canshu = {}
            card_feed = (i.find('.card-feed'))
            content = card_feed.find('.content')
            name = content.find('.name').text()
            name_link = content.find('.name').attr('href')
            txt = content.find('.txt').text()
            weibo_from = content.find('.from').text()

            card_act = i.find(('.card-act'))
            feed_list_forward = 0
            feed_list_comment = 0
            feed_list_like = 0
            for i in card_act.find('li').items():
                # print(i.text())
                if '转发' in i.text():
                    feed_list_forward = (i.text()).replace('转发', '')
                    continue
                elif '评论' in i.text():
                    feed_list_comment = (i.text()).replace('评论', '')
                    continue

                feed_list_like = (i.text())
            if feed_list_forward == '':
                feed_list_forward = 0
            if feed_list_comment == '':
                feed_list_comment = 0
            if feed_list_like == '':
                feed_list_like = 0
            print(name, name_link, weibo_from, feed_list_forward, feed_list_comment, feed_list_like)
            canshu['page_url'] = pageurl
            canshu['name'] = name
            canshu['name_link'] = name_link
            canshu['weibo_from'] = weibo_from
            canshu['txt'] = txt
            canshu['feed_list_forward'] = feed_list_forward
            canshu['feed_list_comment'] = feed_list_comment
            canshu['feed_list_like'] = feed_list_like
            canshu['search_time'] = begintime
            canshu_list.append(canshu)
        self.canshu_queue.put(canshu_list)

    def req_index(self):
        while True:
            if self.urlqueue.qsize()%5==0:
                sleep(10)
            task_item=self.urlqueue.get()
            url=task_item.get('url')
            flag=task_item.get('flag')
            id=task_item.get('id')
            time=task_item.get('time')
            pageurl = str(url).replace("indexpage", str(1))
            data = self.get_data(pageurl)
            doc = pq(data)
            pl_feedlist_index = doc.find('#pl_feedlist_index')
            if pl_feedlist_index.find('.card-no-result'):
                self.urlqueue.task_done()
                weibo_task =session.query(WeiboTask).filter_by(id=id).first()
                weibo_task.flag='5'
                session.commit()
                continue
            page=1
            for i in pl_feedlist_index.find('.m-page .list .s-scroll li').items():
                page = i.text().replace('第', '').replace('页', '')
                print(page)
            if int(page) > 0:
                weibo_task = session.query(WeiboTask).filter_by(id=id).first()
                weibo_task.flag = '1'
                session.commit()
                for page_num in range(1, int(page) + 1):
                    sec_url_item={}
                    pageurl = str(url).replace("indexpage", str(page_num))
                    sec_url_item['id']=id
                    sec_url_item['url']=pageurl
                    sec_url_item['time']=time
                    self.sec_urlqueue.put(sec_url_item)
            self.urlqueue.task_done()


    def seconde_run(self):
        while True:
            sec_task_item =self.sec_urlqueue.get()
            pageurl =sec_task_item.get('url')
            time =sec_task_item.get('time')
            id =sec_task_item.get('id')
            data = self.get_data(pageurl)
            doc = pq(data)
            pl_feedlist_index = doc.find('#pl_feedlist_index')
            if pl_feedlist_index.find('.card-no-result'):
                self.sec_urlqueue.task_done()
                continue
            self.parse_html(pl_feedlist_index,time,pageurl)
            self.sec_urlqueue.task_done()

    def insert(self):
        while True:
            canshu_list =self.canshu_queue.get()
            for canshu in canshu_list:
                weibo_info = WeiboInfo()
                weibo_info.page_url = canshu.get('page_url')
                weibo_info.name = canshu.get('name')
                weibo_info.name_link = canshu.get('name_link')
                weibo_info.weibo_from = canshu.get('weibo_from')
                weibo_info.txt = canshu.get('txt')
                weibo_info.feed_list_forward = canshu.get('feed_list_forward')
                weibo_info.feed_list_comment = canshu.get('feed_list_comment')
                weibo_info.feed_list_like = canshu.get('feed_list_like')
                weibo_info.search_time = canshu.get('search_time')
                self.session.add(weibo_info)
                self.session.flush()
            self.session.commit()
            self.canshu_queue.task_done()

    def run(self):
        weibotask = self.session.query(WeiboTask).filter(WeiboTask.flag == '0').order_by(WeiboTask.time.desc()).all()
        for i in weibotask:
            task_item={}

            task_item['id']=i.id
            task_item['url']=i.url
            task_item['flag']=i.flag
            task_item['time']=i.time
            self.urlqueue.put(task_item)

        thread_list =[]
        for i in range(1):
            Treq_page = threading.Thread(target=self.req_index)
            thread_list.append(Treq_page)
        for i in range(100):
            secTreq_page = threading.Thread(target=self.seconde_run)
            thread_list.append(secTreq_page)
        for i in range(1):
            sqlTreq_page = threading.Thread(target=self.insert)
            thread_list.append(sqlTreq_page)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for q in [self.urlqueue,self.sec_urlqueue,self.canshu_queue]:
            q.join()


if __name__ == '__main__':
    weib = Weibo()
    weib.run()
