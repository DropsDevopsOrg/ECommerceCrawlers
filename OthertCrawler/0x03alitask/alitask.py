import requests
import time
import random
import re
from openpyxl import Workbook


for i in range(1, 5):
    time.sleep(1)
    url = "https://v.taobao.com/micromission/req/selectCreatorV3.do"
    time_tup = str(time.time())
    randoms = random.randint(10, 98)
    timechuo = time_tup[0:10] + time_tup[11:13] + "_" + str(randoms)
    data = {
        'cateType': '801',
        'role': '型男',
        'currentPage': i,
        '_ksTS': timechuo,
        'callback': 'jsonp' + str(randoms + 1),
        '_output_charset': 'UTF-8',
        '_input_charset': 'UTF-8'
    }
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

    respons = requests.get(url, params=data, headers=headers,verify=False)
   # print(respons.text)

    # 名称
    content_name = re.findall('"nick":"(.*?)"', respons.text)
    print("所有名称：", content_name)

    # 服务评分
    content_score = re.findall('"avgScore":"(.*?)"', respons.text)

    # 粉丝数
    content_fans = re.findall('"fansCount":"(.*?)"', respons.text)

    # 合作任务数
    content_cooperate = re.findall('合作任务数","value":"(.*?)"', respons.text)

    # 任务完成率
    content_complete_rate = re.findall('任务完成率","value":"(.*?)"', respons.text)

    # 垂直领域
    content_type = re.findall('"servType":"(.*?)"', respons.text)

    # 7日浏览次数
    content_watch = re.findall('图文7日浏览次数","value":"(.*?)"', respons.text)

    users = []  # 用户数量数组
    servers = []  # 服务数量数组

    home_url = re.findall(',"homeUrl":"(.*?)"', respons.text)
    userId = re.findall('userId=(.*?)&', str(home_url))
    http = 'https://v.taobao.com/micromission/daren/daren_main_portalv3.do?'
    spm = '1xh.11312877.801.1.5a442501GQXmTa'

    for i in range(0, 20):
        time_tup2 = str(time.time())
        randomss = random.randint(10, 98)
        timechuo2 = time_tup2[0:10] + time_tup2[11:13] + "_" + str(randomss)
        callback = "jsonp" + str(randomss + 1)

        # 构造新的url
        new_url = http + 'userId=' + userId[i] + '&spm=' + spm + '&_ksTS=' + timechuo2 + '&callback=' + callback

        respons2 = requests.get(new_url, headers=headers,verify=False)

        countuser = re.findall('cooperateSellerCount":(.*?),"', respons2.text)[0]
        countserver = re.findall('completeMission":(.*?),"', respons2.text)[0]

        users.append(countuser)
        servers.append(countserver)
    # print(respons2.text)

    print("users:", users)
    print("servers:", servers)









