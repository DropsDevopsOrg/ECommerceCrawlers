import csv
import os
import re
import warnings

import pandas as pd
import requests
# from getProxies import ProxyIP
from fake_useragent import UserAgent
from scrapy import Selector

warnings.filterwarnings('ignore')

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = ""
proxyPass = ""

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}


class AnJuKe(object):
    def __init__(self):
        self.city_list_url = 'https://www.anjuke.com/sy-city.html'  # 城市列表
        self.city_dict = {}  # 存放城市地址
        # user-agent 与 代理ip池
        # self.proxies_list = ProxyIP().getProxyIPs(100)  # 获取代理ip列表
        self.ua = UserAgent()
        # 存储路径
        self.path = './csv/'

    def get_city_list(self):

        user_agent = self.ua.chrome

        headers = {'sec-fetch-dest': 'document',
                   'sec-fetch-mode': 'navigate',
                   'sec-fetch-site': 'none',
                   'sec-fetch-user': '?1',
                   'upgrade-insecure-requests': '1',
                   'user-agent': user_agent}

        response = requests.get(self.city_list_url, headers=headers)
        sel = Selector(text=response.text)
        city_name = sel.xpath("//div[@class='city_list']/a/text()").extract()  # 获取名字列表
        city_url = sel.xpath("//div[@class='city_list']/a/@href").extract()  # 获取城市路径url
        for i in range(len(city_name)):
            # 创建城市信息列表
            L = [city_name[i], city_url[i]]
            with open(self.path + '全国城市请求地址表.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(L)
        print("-------> 全国城市地址信息存储完毕 <-------")

    def get_agent_list(self, city, city_url, start_page, end_page):
        for page_num in range(start_page, end_page + 1):
            print("正在爬取第{}页经纪人信息".format(str(page_num)))
            user_agent = self.ua.chrome
            agent_url = (city_url + '/tycoon/p{}/').format(str(page_num))  # 获取完整经纪人url

            refer_url = city_url + '/tycoon/?from=navigation' if page_num == 1 else (city_url + '/tycoon/p{}/').format(
                str(page_num - 1))
            # 这里的headers的user-agent也需要进行替换
            headers = {'referer': refer_url,
                       'sec-fetch-dest': 'document',
                       'sec-fetch-site': 'same-origin',
                       'sec-fetch-user': '?1',
                       'upgrade-insecure-requests': '1',
                       'user-agent': user_agent}

            # 请求网页内容获取list(关键是要获取他的扫描二维码的图片地址)
            request_count = 0
            while request_count < 15:
                try:
                    # proxies = random.choice(self.proxies_list)
                    response = requests.get(agent_url, headers=headers, proxies=proxies, timeout=4)
                    # 尝试请求十次，如果不成功，则放入异常中
                    if (response.status_code == 200) and ('访问验证' not in response.text):
                        if ('哎呀，没有找到符合要求的经纪人' in response.text):
                            request_count += 1
                        else:
                            break
                    else:
                        request_count += 1
                except:
                    request_count += 1

            # 想要的是jjr-数字的信息
            sel = Selector(text=response.text)
            jjr_url_list = sel.xpath("//div[@class='jjr-info']//h3/a/@href").extract()  # phone_url
            # 对最后的页面进行判断
            if len(jjr_url_list) > 0:
                jjr_name_list = sel.xpath("//div[@class='jjr-info']//h3/a/@title").extract()  # name_list
                # 请求新的weixin网址获取电话数据
                jjr_company_url = sel.xpath("//div[@class='jjr-info']//h3/a/@href").extract()  # company_list
                self.get_agent_info(jjr_url_list, jjr_name_list, jjr_company_url, city)
            else:
                # 判断是否是人机验证
                if ('访问验证' in response.text):
                    print("----->出现人机验证，经纪人列表地址加入加入log日志中<------")
                    with open(self.path + 'error.csv', 'a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow([city, agent_url])
                # 这里是判断既不是人机验证，是无合适经纪人
                else:
                    print("{}无经纪人信息".format(city))
                    break

    def get_agent_info(self, agent_jjr_list, agent_name_list, jjr_company_list, city):

        agent_dict = {}

        for i in range(len(agent_jjr_list)):
            # 获取随机user-agent 和 proxies
            user_agent = self.ua.chrome
            # response = ''

            headers = {'sec-fetch-dest': 'document',
                       'sec-fetch-mode': 'navigate',
                       'sec-fetch-site': 'same-site',
                       'sec-fetch-user': '?1',
                       'upgrade-insecure-requests': '1',
                       'user-agent': user_agent}

            re_match = re.compile('jjr\-\d+')  # 匹配后面的内容
            jjr_num = re.findall(re_match, agent_jjr_list[i])[0]
            # 请求公司信息的详情网址
            company_name, company_shop, company_card, service_year, info_url = self.get_company_info(
                jjr_company_list[i])

            # 请求电话详情的网址
            phone_url = 'https://m.anjuke.com/as/{}/'.format(jjr_num)
            # print("------->当前请求的电话地址为:{}<--------".format(info_url))
            request_count = 0
            while request_count < 15:
                try:
                    # proxies = random.choice(self.proxies_list)
                    response = requests.get(phone_url, headers=headers, proxies=proxies, timeout=4)
                    # 判断成功响应，且没有出现验证信息
                    if (response.status_code == 200) and ('访问验证' not in response.text):
                        break
                    else:
                        request_count += 1
                except:
                    request_count += 1
            # 正则获取电话号码
            phone_num = self.get_phone_num(response.text)
            agent_dict[agent_name_list[i]] = phone_num
            # 写入信息
            L = [agent_name_list[i] + '的店铺', phone_num, company_name, company_shop, company_card, service_year,
                 info_url]
            if not os.path.exists('./csv/{}.csv'.format(city)):
                with open('./csv/{}.csv'.format(city), 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['店铺名称', '手机号', '公司名称', '公司店铺', '公司执照', '服务年限', '详情链接'])
            else:
                with open('./csv/{}.csv'.format(city), 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(L)
                print(L)

        print("数据写入完毕，此页信息为:", agent_dict)
        print("-" * 100)

    def get_company_info(self, jjr_company_url):
        info_url = jjr_company_url + 'js/'
        user_agent = self.ua.chrome
        # response = ''  # 定义一个局部变量

        headers = {'refer': jjr_company_url,
                   'sec-fetch-dest': 'document',
                   'sec-fetch-mode': 'navigate',
                   'sec-fetch-site': 'same-site',
                   'sec-fetch-user': '?1',
                   'upgrade-insecure-requests': '1',
                   'user-agent': user_agent}

        request_count = 0
        while request_count < 15:
            try:
                # proxies = random.choice(self.proxies_list)
                response = requests.get(info_url, headers=headers, proxies=proxies, timeout=4)
                if response.status_code == 200 and ('访问验证' not in response.text):
                    sel = Selector(text=response.text)
                    company_name = sel.xpath("//div[@class='item-content']//a/text()").extract_first()  # 获取公司信息
                    if company_name:
                        break
                    else:
                        request_count += 3
            except:
                request_count += 1

        sel = Selector(text=response.text)
        company_name = sel.xpath("//div[@class='item-content']//a/text()").extract_first()  # 获取公司信息
        # 请求信息
        try:
            company_shop = sel.xpath("//div[@class='item-content']//span/text()").extract_first()  # 获取公司门店信息
            company_card = sel.xpath("//div[@class='card-info']/p/text()").extract()  # 获取公司执照信息
            # 若果匹配长度
            if company_card:
                company_card = company_card[1] if len(company_card) > 1 else company_card[0]
            else:
                company_card = ''
            service_year = sel.xpath("//span[@class='item-txt']/text()").extract_first()  # 获取公司
            return company_name.strip(), company_shop.strip(), company_card, service_year, info_url
        except Exception as e:
            return '', '', '', '', info_url

    def get_phone_num(self, text):
        # 先获取一层
        try:
            re_match = re.compile('"title":[\s\S]*?",')
            info_title = re.findall(re_match, text)[0]
            # 再获取一层
            re_match_num = re.compile('1\d{10}')
            phone_num = re.findall(re_match_num, info_title)[0]
            return phone_num
        except Exception as e:
            return ''

    def get_city_url(self):
        data = pd.read_csv('全国城市请求地址表.csv')
        for index in data['城市'].index:
            self.city_dict[data['城市'].at[index]] = data['网址'].at[index]

    def run(self):
        self.get_city_url()  # 运行得到所有城市列表
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            print("csv文件夹创建成功")

        city = input("请输入您所需要爬取的城市名称: ")
        # 从列表中获取(省会城市)
        city_url = self.city_dict[city]
        start_page = input("请输入您想爬取的起始页码数: ")
        end_page = input("请输入您想爬取的终止页码数(小于等于50): ")
        # 请求经纪人列表
        self.get_agent_list(city, city_url, int(start_page), int(end_page))


if __name__ == '__main__':
    ajk = AnJuKe()
    ajk.run()
