#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/5/9 0009'

"""
#配置信息
'''
爬取手机端的接口信息，
 "http://v2.sohu.com/integration-api/mix/region/84?size=100",
爬取方式，
    获取每天的最新的新闻，一般200篇就
    一般情况可以获取100多个页面新闻的链接
    对比对应的set集合有没有连接
    没有连接就存入数据库，存入待爬取的数据库
    然后集合中加入此链接
    
    爬取模块，定期从数据库中找到是否存在带爬取的链接 - 时间间隔可以程序自动调整
'''

# 可以遍历1-133篇文章的url
new_url_list=["http://v2.sohu.com/integration-api/mix/region/"]

# 每天的新闻量
size=200

type_name='souhu'