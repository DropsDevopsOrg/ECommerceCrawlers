# -*- coding: utf-8 -*-
import scrapy
from cnblog.items import CnblogItem


class CnblogSpiderSpider(scrapy.Spider):
    name = "cnblog_spider"
    allowed_domains = ["cnblogs.com"]
    url = 'https://www.cnblogs.com/sitehome/p/'
    offset = 1
    start_urls = [url+str(offset)]

    def parse(self, response):


        item = CnblogItem()

        item['title'] = response.xpath('//a[@class="titlelnk"]/text()').extract()       #使用xpath搜索
        item['link'] = response.xpath('//a[@class="titlelnk"]/@href').extract()

        yield item

        print("第{0}页爬取完成".format(self.offset))
        if self.offset < 10:        #爬取到第几页
            self.offset += 1
        url2 = self.url+str(self.offset)    #拼接url
        print(url2)
        yield scrapy.Request(url=url2, callback=self.parse)

