import os
import requests
from config import *
from lxml import etree
import csv
from fake_useragent import UserAgent


def get_parks(num_page):
    url = "https://www.qichacha.com/more_zonesearch.html?searchKey=&p={}".format(
        num_page)

    ua = UserAgent(verify_ssl=False)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'DNT': '1',
        'Host': 'www.qichacha.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
        'User-Agent': ua.random
    }

    # response = requests.get(url, headers=headers, proxies=proxies)
    response = requests.get(url, headers=headers)

    html = response.text
    # print(html)
    parseHtml = etree.HTML(html)

    # '/zonecompany_02212bebbb2c3b0212c7652e6feaeacf'
    rUrls = parseHtml.xpath('//div[@class="panel n-s m-t-md"]/a/@href')
    # '\n                    银江科技产业园\n                  '
    rTitle = parseHtml.xpath(
        '//div[@class="panel n-s m-t-md"]/a/div[@class="ea_title"]/text()')
    # '省份：浙江省'
    rProvince = parseHtml.xpath(
        '//div[@class="panel n-s m-t-md"]/a/div[@class="clearfix"][1]/span[1]/text()')
    # '城市/区：杭州市, 西湖区'
    rCityCounty = parseHtml.xpath(
        '//div[@class="panel n-s m-t-md"]/a/div[@class="clearfix"][1]/span[2]/text()')
    # '占地面积：9亩'
    rArea = parseHtml.xpath(
        '//div[@class="panel n-s m-t-md"]/a/div[@class="clearfix"][2]/span[1]/text()')
    # '企业数：278家'
    rNumCop = parseHtml.xpath(
        '//div[@class="panel n-s m-t-md"]/a/div[@class="clearfix"][2]/span[2]/text()')

    path = './csv/'
    # 判断\新建文件夹
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, ' 文件夹创建成功')
    file_name = path+parks_name+'.csv'
    # 判断\新建文件
    if not os.path.exists(file_name):
        header = ['province', 'city', 'county',
                  'park', 'area', 'numcop', 'url']
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)

    num = len(rUrls)
    for i in range(num):
        url = 'https://www.qichacha.com' + rUrls[i]
        park = rTitle[i].replace('\n', '').strip()
        province = rProvince[i].replace('省份：', '')
        city = rCityCounty[i].replace('城市/区：', '').split(', ')[0]
        county = rCityCounty[i].replace('城市/区：', '').split(', ')[-1]
        area = int(rArea[i].replace('占地面积：', '').replace('亩', ''))
        numcop = int(rNumCop[i].replace('企业数：', '').replace('家', ''))
        L = [province, city, county, park, area, numcop, url]
        # print(L)
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(L)

    return num


num_page = 301

Total = 0
for i in range(1, num_page+1):
    num = get_parks(i)
    Total += num
    print('完成爬取页码: {} / {}'.format(i, num_page))

print('全国 工业园区 爬取完成, 企业数目: ', Total)
