#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/4/15 0015'

"""
# 根据关键字查询 导出excel名字
from dbsimil import Mongo
from openpyxl import Workbook
import os

KEYWORD = '关键字'
wb = Workbook()
ws = wb.active
ws.append(["搜索词", "链接", "标题", "价格", "店铺名称", "销量", "同款数", "同款标题", "同款链接", "同款店铺", "同款价格", "同款销量", "找同款链接"])
ws.append([])
save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), KEYWORD + '.xlsx')
wb.save(save_path)