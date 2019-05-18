#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/5/9 0009'

"""

# from pyquery import PyQuery as pq
# import requests
# # start_url = "http://v2.sohu.com/integration-api/mix/region/84?size=100"
# start_url = "https://m.sohu.com/a/312825999_100292554"
# req = requests.get(url=start_url, timeout=30)
# print(req.status_code)
# html =req.text
# d = pq(html)
# text = d('article').text()
# print(text)
#
#
# souhu_json = req.json()
# print(souhu_json)
#
# news_header_list=souhu_json.get('data')
# if news_header_list:
#     for per_new in news_header_list:
#         url = per_new.get("url")
#         title = per_new.get("title")
#         time = per_new.get("publicTime")
# from  urllib import parse
#
# newurl = parse.urljoin('https://m.sohu.com','https//m.sohu.com/promotion?link=ND059%2BeCDpgdHfuuomLUfdWSWHD%2F%2FJh7Ei43qlyJ%2B63NwWjibrTtlkhVj%2Fu9D9oS5J%2F2A58%2F8RUiHU%2BlXo%2BYa0RrqaIluNhz%2Fk3zw5PcKZ%2FhZQom%2BEVfxDLSW8e3PnTQUa6ZrDmdL12IePfg716oQefK%2FVdP8KovqhXC449Skoo%3D')
# url='http://use'
# parsed_result = parse.urlparse(url)
#
# scheme = parsed_result.scheme
# print(scheme)
# print(newurl)
#
# from urllib.parse import urlparse
#
# url='http://user:pwd@domain:80/path;params?query=queryarg#fragment'
#
# parsed_result=urlparse(url)
#
# print('parsed_result 包含了',len(parsed_result),'个元素')
# print(parsed_result)
# print('scheme  :', parsed_result.scheme)
import os
base_path = os.path.abspath(os.path.dirname(__file__))

file_size = 300 * 1024
save_path = os.path.join('D:\\Python_program\\Spider\\all_news','news')
print(save_path)
def less_file_size(save_path):
    for root ,dirnames, file_paths in os.walk(save_path):
        print(root)
        for file_path in file_paths:
            print(file_path)
            ds = os.path.getsize(os.path.join(root,file_path))
            if ds<file_size:
                print('小于300kb',file_path)
                return os.path.join(root,file_path)

print('继续添加',less_file_size(save_path))