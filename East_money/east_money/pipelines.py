# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os


class EastMoneyPipeline(object):
    def process_item(self, item, spider):
        os.chdir('E:/Ana project/east_money/result_txt')
        with open(item['title']+ '.txt', 'a', encoding='utf-8') as f:
            f.write('新闻链接：'+item['href']+'\n')
            if item['summary']:
                f.write(item['summary']+ '\n')
            else:
                f.write('此新闻没有摘要' + '\n')
            f.write(item['content'] + '\n')
        return item
