import requests
from lxml import etree

for i in range(1, 126):
    print('page:\t', i)
    url = 'https://bing.ioliu.cn/?p={}'.format(i)

    headers = {
        'Host': 'bing.ioliu.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Sec-Fetch-Dest': 'document',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '_ga=GA1.2.1389080226.1586346124; _gid=GA1.2.1179718529.1586346124; Hm_lvt_667639aad0d4654c92786a241a486361=1586346124; likes=; Hm_lpvt_667639aad0d4654c92786a241a486361=1586347115',
        'If-None-Match': 'W/"5ae9-A6K6aP64lqd/8LCoQ4XYnQ"'
    }
    res = requests.get(url, headers=headers, verify=False)
    # print(res.text)
    parseHtml = etree.HTML(res.text)
    picList = parseHtml.xpath('//img/@src')
    # print(picList)
    for pic in picList:
        try:
            # http://h1.ioliu.cn/bing/SantoriniAerial_ZH-CN9367767863_640x480.jpg?imageslim
            picUrl = pic.split('_640')[0] + '_1920x1080.jpg'
            picName = pic.split('bing/')[-1].split('_')[0] + '.jpg'
            picRes = requests.get(picUrl)
            with open(picName, 'wb') as f:
                f.write(picRes.content)

        except Exception as e:
            print(i, pic, e)
