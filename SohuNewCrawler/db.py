#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/5/9 0009'

"""
from pymongo import MongoClient, ASCENDING

# 打包服务
# mongod.exe --logpath D:\mongodb\xianyudb\mongodb.log --logappend --dbpath D:\mongodb\xianyudb --directoryperdb --serviceName mongodbxy --install

ip = '127.0.0.1'
port = 27017

# url链接的存储
class MongoUrl():
    def __init__(self, ip=ip, port=port):
        conn = MongoClient(ip, port)
        self.db = conn.News
        self.collection = self.db.new_url
        self.collection.create_index([('nid', ASCENDING)])

    def insert(self, item_dict):
        # 插入数据
        self.collection.insert_one(item_dict)

    def select_one(self, dict):
        return self.collection.find_one(dict)

    def select(self, dict):
        # 自定义选择数据
        return self.collection.find(dict)

    def delete(self, query_dict):
        self.collection.delete_one(query_dict)

    def delete_all(self, dict):
        #
        self.collection.delete_many(dict)

    def find_one_update_flag1(self):
        return self.collection.find_one_and_update({"flag": 0}, {'$set': {"flag": 1}})

    def update_url_flag0(self, url):
        self.collection.update({'url': url}, {'$set': {"flag": 0}})

    def update(self, dict):
        self.collection.update(dict)

    def count(self):
        self.collection.count_documents({})

# 文章的操作
class MongoArticle():
    def __init__(self, ip=ip, port=port):
        conn = MongoClient(ip, port)
        self.db = conn.News
        self.collection = self.db.new_article
        self.collection.create_index([('nid', ASCENDING)])

    def insert(self, item_dict):
        self.collection.insert_one(item_dict)

    def select_one_update(self):
        return self.collection.find_one_and_update({"flag": 0}, {'$set': {"flag": 1}})

    def select_by_time(self,time):
        return self.collection.find({"time":time})

    def select_all(self):
        return self.collection.find()

    def delete_all(self, dict):
        #
        self.collection.delete_many(dict)

class MongoConfig():
    def __init__(self, ip=ip, port=port):
        conn = MongoClient(ip, port)
        self.db = conn.News
        self.collection = self.db.new_config
        self.collection.create_index([('nid', ASCENDING)])

    def insert(self, item_dict):
        self.collection.insert_one(item_dict)
    def select_one(self):
        return self.collection.find_one({"flag":1})
    def select_one_update(self):
        return self.collection.find_one_and_update({"flag": 0}, {'$set': {"flag": 1}})

    def select_by_time(self,time):
        return self.collection.find({"time":time})

    def select_all(self):
        return self.collection.find()

    def update(self, thread,time,path):
        self.collection.update({'flag': 1}, {'$set': {"thread": thread,"time":time,"path":path}})

    def delete_all(self, dict):
        #
        self.collection.delete_many(dict)

if __name__ == '__main__':
    db_mu = MongoUrl()
    db_ma = MongoArticle()

    # 插入的数据:{"url":"待爬取的新闻链接","time":'2019-05-03 01:32:00',"flag":是否被爬取标志0,"title":"标题","type":"新闻来源百度新闻"}
    # db_mu.insert({"url":"http://www.baidu.com","time":'2019-05-03 01:32:00',"flag":0,"title":"暂无","type":"baidu_new百度新闻"})

    #{"articel":"一段内容","flag":是否被导出,"time":"2019-05-03 01:32:00","title":"暂无","type":"新闻来源百度新闻","url":"新闻链接"}
    # db_ma.insert({"articel":"一段过滤后的内容","flag":0,"time":"2019-05-03 01:32:00","title":"暂无","type":"baidu_new百度新闻","url":"http://www.baidu.com"})

    #取出一个url并更新为已经爬取
    # no_spider_url = db_mu.find_one_update_flag1()
    # if no_spider_url:
    #     url = no_spider_url.get("url")
    #     print(url)