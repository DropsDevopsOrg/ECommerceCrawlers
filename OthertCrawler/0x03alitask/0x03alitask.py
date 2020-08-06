import os
import random
import re
import time

import requests
from openpyxl import Workbook


# 爬取数据
def spider(sheet):
    # 定义爬取页数
    for page in range(1, 3):
        time.sleep(1)
        time_chuo = str(time.time()).split('.')

        randoms = random.randint(50, 100)
        payload_time = time_chuo[0] + time_chuo[1][:3] + '_' + str(randoms)

        url = 'https://v.taobao.com/micromission/req/selectCreatorV3.do'

        headers = {
            'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': 'v=0; cookie2=1d8e5b2722a0d96318231f74a248baba; t=bf69902d83642741a1cc6b339022fd16; _tb_token_=7e5133b8ee8a1; cna=6b8kFaItdRwCAXs0aVrjLweG; JSESSIONID=710CA60FCD29541A182EDF2E1F5C4913; uc1=cookie14=UoTZ50E5LAt0CA%3D%3D; l=bBOd-SElv4iGbbChBOfiNZ6B1ab9PIdbz1PPhjjiOICPO4fwfwwOWZ6QTPYeC3GVa6LWR3ouEw9UB58seyUBl; isg=BLOzYeaj68ciWqcThG5A6os-QrfXbUhkWwwRY2VRqlIjZNAG7bri-uOyHtQvQ5-i',
            'pragma': 'no-cache',
            'referer': 'https://v.taobao.com/v/content/graphic',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        query_string = {
            'cateType': '801',
            'role': '型男',
            'currentPage': '%d' % page,
            '_ksTS': '%s' % payload_time,
            'callback': 'jsonp%d' % (randoms + 1),
            '_output_charset': 'UTF-8',
            '_input_charset': 'UTF-8'
        }

        req = requests.get(url, params=query_string, headers=headers, verify=False)

        # 名称
        content_name = re.findall('"nick":"(.*?)"', req.text)

        # 服务评分
        content_score = re.findall('"avgScore":"(.*?)"', req.text)

        # 粉丝数
        content_fans = re.findall('"fansCount":"(.*?)"', req.text)

        # 合作任务数
        content_cooperate = re.findall('合作任务数","value":"(.*?)"', req.text)

        # 任务完成率
        content_complete_rate = re.findall('任务完成率","value":"(.*?)"', req.text)

        # 垂直领域
        content_type = re.findall('"servType":"(.*?)"', req.text)

        # 7日浏览次数
        content_watch = re.findall('图文7日浏览次数","value":"(.*?)"', req.text)

        # 二次爬虫
        # 获取所有url，这个url并没有累计用户数的信息，另一个网址有累计用户数，但另一个网址需要这个url的参数，因此需要重新构造url
        home_url = re.findall('homeUrl":"(.*?)"', req.text)
        # 获取userId
        userId = re.findall('userId=(.*?)&', str(home_url))
        spm = 'a21xh.11312877.801.1.5a442501LfEm2o'

        # 定义一个列表保存累计用户数的数据
        cooperateSellerCount = []
        for i in range(0, 20):
            # 构造时间戳
            time_chuo = str(time.time()).split('.')
            randoms = random.randint(50, 100)
            payload_time = time_chuo[0] + time_chuo[1][:3] + '_' + str(randoms)
            # 构造callback
            callback = 'jsonp%d' % (randoms + 1)

            # 构造新的url，可以获取到累计用户数
            new_url = 'https://v.taobao.com/micromission/daren/daren_main_portalv3.do?userId=' + userId[
                i] + '&spm=' + spm + '&_ksTS=' + payload_time + '&callback=' + callback
            res = requests.get(new_url, headers=headers, verify=False)
            data = re.findall('cooperateSellerCount":(.*?),"', res.text)[0]
            cooperateSellerCount.append(data)

        print('已爬取到Page %d的数据！正在写入' % page)

        # 写入数据
        for i in range(0, 20):
            single_list = []
            single_list.append(content_name[i])
            single_list.append(content_score[i])
            single_list.append(content_fans[i])
            single_list.append(content_cooperate[i])
            single_list.append(content_complete_rate[i])
            single_list.append(content_type[i])
            single_list.append(content_watch[i])
            single_list.append(cooperateSellerCount[i])

            sheet.append(single_list)

        print('写入成功！')


# 初始表格
wb = Workbook()
sheet = wb.active
sheet.title = '爬取的数据sheet'
name = ['达人名称', '服务评分', '粉丝数量', '合作任务', '完成比率', '垂直领域', '累计浏览', '累计用户']
sheet.append(name)

# 爬取、写入数据
spider(sheet)

# 创建文件夹
try:
    os.chdir('D:\\')
    os.mkdir('Spider_test1')
    os.chdir('D:\\Spider_test1')
except Exception as e:
    os.chdir('D:\\Spider_test1')

# 保存为表格
try:
    wb.save('spider.xlsx')
except Exception as f:
    os.remove('spider.xlsx')
    wb.save('spider.xlsx')

print('数据已保存在D盘Spider_test1文件夹内！')
