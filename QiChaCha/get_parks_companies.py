import os
import requests
from config import *
from lxml import etree
import csv
from fake_useragent import UserAgent
import pandas as pd

ua = UserAgent(verify_ssl=False)
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': cookie,
    'DNT': '1',
    'Host': 'www.qichacha.com',
    'Referer': 'https://www.qichacha.com/more_zonecompany.html?id=000c85b2a120712454f4c5b74e4fdfae&p=2',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    'User-Agent': ua.random
}

path = './csv/'
file_name = path+companies_name+'.csv'


def get_companies(id, page_no):
    url = 'https://www.qichacha.com/more_zonecompany.html?id={}&p={}'.format(
        id, page_no)
    # response = requests.get(url, headers=headers, proxies=proxies)
    response = requests.get(url, headers=headers)
    html = response.text
    parseHtml = etree.HTML(html)

    return parseHtml


def get_companies_all(id, province, city, county, park, area, numcop):
    parseHtml = get_companies(id, 1)

    # ['\n                                    71\n                                ']
    rNum = parseHtml.xpath(
        '//div[@class="e_zone-company"]/div[1]/span/span/text()')
    _num = int(rNum[0].replace('\n', '').strip())

    num_page = _num // 10 + 1

    for i in range(1, num_page+1):
        # for i in range(1, 2):
        parseHtml = get_companies(id, i)
        # '/firm_2468290f38f4601299b29acdf6eccce9.html'
        rUrls = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/a/@href')
        # '临海市互通汽车销售有限公司'
        rTitle = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/a/text()')
        # '黄剑勇'
        rPerson = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/p[1]/a/text()')
        # '注册资本：1000万元人民币'
        rCapital = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/p[1]/span[1]/text()')
        # '成立日期：2017-09-08'
        rSetTime = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/p[1]/span[2]/text()')
        # '\n              邮箱：3093847569@QQ.COM\n               '
        rEmail = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/p[2]/text()')
        # '电话：0576-85323665'
        rPhone = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/p[2]/span/text()')
        # '\n         地址：浙江省台州市临海市江南街道恒大家居建材城(靖江南路112号)\n       '
        rAddress = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[2]/p[3]/text()')
        # '存续'
        rState = parseHtml.xpath(
            '//div[@class="e_zone-company"]/section/table/tbody/tr/td[3]/span/text()')

        num_current = len(rUrls)
        for num in range(num_current):
            try:
                url = 'https://www.qichacha.com'+rUrls[num]
                company = rTitle[num]
                person = rPerson[num]
                capital = rCapital[num].replace('注册资本：', '')
                settime = rSetTime[num].replace('成立日期：', '')
                email = rEmail[num].replace(
                    '\n', '').replace('邮箱：', '').strip()
                phone = rPhone[num].replace('电话：', '')
                address = rAddress[num].replace(
                    '\n', '').replace('地址：', '').strip()
                state = rState[num]
                L = [province, city, county, park, area, numcop, company,
                     person, capital, settime, email, phone, address, state, url]
                with open(file_name, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(L)
            except Exception as e:
                err_log(id, i)
                print('报错 ID: {} , 页码: {} / {}'.format(id, i, num_page))
        print('完成爬取 ID: {} , 页码: {} / {}'.format(id, i, num_page))


def err_log(id, page):
    err_file = path + 'error.csv'
    if not os.path.exists(err_file):
        header = ['id', 'page']
        with open(err_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    with open(err_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([id, page])


def work():

    # 判断\新建文件夹
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, ' 文件夹创建成功')

    # 判断\新建文件
    if not os.path.exists(file_name):
        header = ['province', 'city', 'county', 'park', 'area', 'numcop', 'company',
                  'person', 'capital', 'settime', 'email', 'phone', 'address', 'state', 'url']
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)

    csv_data = pd.read_csv('./csv/全国工业园区信息.csv')
    length = len(csv_data)
    for i in range(length):
        province = csv_data.loc[i, 'province']
        city = csv_data.loc[i, 'city']
        county = csv_data.loc[i, 'county']
        park = csv_data.loc[i, 'park']
        area = csv_data.loc[i, 'area']
        numcop = csv_data.loc[i, 'numcop']
        id = csv_data.loc[i, 'url'].split('_')[-1]

        get_companies_all(id, province, city, county, park, area, numcop)
        print('\n\n完成爬取 ID: {}, 整体进度: {} / {}\n\n=============================\n'.format(id, i+1, length))


if __name__ == "__main__":
    work()
