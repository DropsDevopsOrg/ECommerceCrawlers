# -*- coding: UTF-8 -*-
__author__ = 'Joynice'

import requests
from utils.utils import get_header
import csv
import os
from lxml.html import etree
import config

class ZhiLian(object):
    '''
    智联招聘
    :param
    构造函数:
    传入：搜索职业关键字、招聘地点
    调用run方法：返回csv文件
    '''
    def __init__(self, keyword, page=100, city='全国', path=os.getcwd()):
        self.keyword = keyword
        self.page = page
        self.base_url = 'https://fe-api.zhaopin.com/c/i/sou'
        self.city = city
        self.csv_header = ['ID', '工作名称', '招聘详细链接', '公司名称', '公司ID', '公司性质', '公司规模', '公司招聘主页',
                           '公司地点', '薪资', '学历要求', '工作经历', '职位类型', '公司福利', '工作发布标签', '更新时间', '职位描述']
        self.path = path


    def Spider(self):
        jobl = []
        for page in range(self.page):
            params = {
                "start": 90 * page,
                "pageSize": 90,
                "workExperience": -1,
                "education": -1,
                "companyType": -1,
                "employmentType": -1,
                "jobWelfareTag": -1,
                "kw": self.keyword,
                "kt": 3,
                "cityId": self.city,
                "salary": '0, 0'
            }
            req = requests.get(url=self.base_url, params=params, headers=get_header())
            cookie = req.cookies
            print(cookie)
            data = req.json()['data']['results']
            if len(data) != 0:
                for job in data:
                    # print(job)
                    jobd = {}
                    jobd['ID'] = job.get('number')
                    jobd['工作名称'] = job.get('jobName')
                    jobd['招聘详细链接'] = job.get('positionURL')
                    company = job.get('company')
                    jobd['公司名称'] = company.get('name')
                    jobd['公司ID'] = company.get('number')
                    jobd['公司性质'] = company.get('type').get('name')
                    jobd['公司规模'] = company.get('size').get('name')
                    jobd['公司招聘主页'] = company.get('url')
                    jobd['公司地点'] = job.get('city').get('display')
                    jobd['薪资'] = job.get('salary')
                    jobd['学历要求'] = job.get('eduLevel').get('name')
                    try:
                        jobd['工作经历'] = job.get('workingExp').get('name')
                    except:
                        jobd['工作经历'] = '经验不限'
                    jobd['职位类型'] = job.get('emplType')
                    jobd['公司福利'] = '、'.join(job.get('welfare')) or '无'
                    jobd['工作发布标签'] = job.get('timeState')
                    jobd['更新时间'] = job.get('updateDate')
                    header = get_header()
                    header['referer'] = job.get('positionURL')
                    header['upgrade-insecure-requests'] = '1'
                    header['cookie'] = config.ZHILIAN_COOKIE
                    req1 = requests.get(job.get('positionURL'), headers=header, )
                    req1.encoding = 'utf-8'
                    html = etree.HTML(req1.text)
                    detail = ''.join(html.xpath('//*[@class="describtion__detail-content"]//*/text()'))
                    if not detail:
                        detail = ''.join(html.xpath('//*[@class="describtion__detail-content"]/text()'))
                    print(detail)
                    jobd['职位描述'] = detail.strip()
                    jobl.append(jobd)
            else:
                break
        return jobl

    def run(self):

        if os.path.exists(self.path):
            data = self.Spider()
            self.path = os.path.join(self.path, 'save-data')
            with open(os.path.join(self.path, '智联招聘_关键词_{}_城市_{}.csv'.format(self.keyword, self.city)), 'w',
                      newline='', encoding='utf-8-sig') as f:
                f_csv = csv.DictWriter(f, self.csv_header)
                f_csv.writeheader()
                f_csv.writerows(data)


if __name__ == '__main__':

    a = ZhiLian(keyword='python', city='南京').run()
