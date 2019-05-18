#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/4/16 0016'

"""
from settings import CONFIG,configdb

from settings import USERINFO

from  settings import KEYWORD

# 关键字
for key in KEYWORD:
    print(key.get("keyword"))

# keywordb.delete({})
# for i in ["牙刷",'牙膏','汽车','袜子']:
#     keywordb.insert({"keyword":i})

# 用户信息
for user in USERINFO:
    username = user.get('username')
    password = user.get('password')
    print('用户',username)
    print(password)


# userinfodb.delete({})
# userinfodb.insert({"username":"15993248973","password":"Bu19951218."})

print((CONFIG))
# 配置信息
# c =  CONFIG
# print('线程',c.get('theadnum',''))
# print(c.get('salenum'))
#
# configdb.delete({})
# #
configdb.insert({"threadnum":5,"salenum":50,"flag":1})

# configdb.update_salenum(49)
# configdb.update_theadnum(3)
from dbcookie import DbClient
cdb  =DbClient()
cdb.delete_all()