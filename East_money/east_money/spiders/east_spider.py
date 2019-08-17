# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from east_money.items import EastMoneyItem
import requests


class EastSpider(scrapy.Spider):
    name = "east"
    allowed_domains = ["stock.eastmoney.com"]
    base_url = 'http://stock.eastmoney.com/news/cmggs_'
    start_urls = []
    item = EastMoneyItem()
    base_url = 'http://stock.eastmoney.com/news/cmggs_'
    intab = "?*/\|.:><"
    outtab = "         "
    trantab = str.maketrans(intab, outtab)  # 制作字符串翻译表，去掉标题中带有的系统敏感字符
    for i in range(1, 11):       # 把每页的url添加到start_urls列表中
        page_url = base_url+str(i)+'.html'
        start_urls.append(page_url)

    def parse(self, response):
        html = response.text
        xpath_tree = etree.HTML(html)
        ul = xpath_tree.xpath('//*[@id="newsListContent"]')  # 获取每页存放着二十条新闻的ul标签
        li_list = ul[0].xpath('./li')  # 获取二十个新闻的li标签
        for li in li_list:
            a_url = li.xpath('.//a[@target="_blank"]/@href')[0]  # 获取每个新闻的ur
            self.spider(url=a_url)
            yield self.item

    def spider(self, url):       # 进行爬取和存储
        print(url)
        self.item['href'] = url         # 存储每条新闻的链接
        html = str(requests.get(url=url).content, encoding='utf-8')
        xpath_tree = etree.HTML(html)
        title = xpath_tree.xpath('/html/body/div[1]/div/div[3]/div[1]/div[2]/div[1]/h1')
        if title:
            pass
        else:
            title = xpath_tree.xpath('/html/body/div[1]/div[3]/div/div[1]/div[1]/div/div[2]/h1')
        title_content = title[0].text.translate(self.trantab)
        self.item['title'] = title_content      # 存储每条新闻的title
        text = xpath_tree.xpath('//*[@id="ContentBody"]')        # 获取正文内容
        if text:
            pass
        else:
            text = xpath_tree.xpath('/html/body/div[1]/div[3]/div/div[1]/div[1]/div/div[3]')
        text_content = text[0]
        summary = text_content.xpath('./div[@class="b-review"]')            # 获取摘要
        if len(summary) > 0:                                    # 判断摘要是否存在
            summary_content = summary[0].text.strip()
            self.item['summary'] = summary_content
        else:
            self.item['summary'] = '该新闻没有摘要'
        p_list = text_content.xpath('./p')          # 获取段落
        content = ''
        for p in p_list:
            p_content = p.xpath('string(.)').strip()+'\n'
            # print(p_content)
            content = content + p_content       # 把段落拼接成一个字符串，每段一行
        self.item['content'] = content


