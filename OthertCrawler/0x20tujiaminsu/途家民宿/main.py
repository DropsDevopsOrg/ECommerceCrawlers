import csv
import pandas
from getItems import getItems
import os

# shanghai beiing guangzhou shenzhen chengdu chongqing qingdao xian wuhan xiamen wulumuqi lasa

city = 'lianyungang'
filename = '途家民宿_/.csv'.replace('/', city)

# List = [unitId, unitName, longitude, latitude, address, unitInfor,
#         productPrice, finalPrice, cityName, districtName, zhengtao, buju, pingfeng, dianping]
if not os.path.exists(filename):
    header = ['unitId', '总数', '标题', '经度', '维度', '地址', '信息',
              '原价', '现价', '城市', '区域', '整套', '布局', '评分', '点评']
    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

while True:
    totalCount, items = getItems(city, 0)
    if totalCount:
        break

maxpage = totalCount // 49 + 1
if maxpage >= 51:
    page = 51
else:
    page = maxpage

for p in range(page):
    print('正在解析第 {} 页, 每页数量 49'.format(p))
    while True:
        totalCount, items = getItems(city, p)
        if totalCount:
            break
    length = len(items)
    for item in items:
        unitId = item['unitId']
        unitName = item['unitName']
        longitude = item['longitude']
        latitude = item['latitude']
        address = item['address']
        unitInfor = item['unitInfor']
        productPrice = item['productPrice']
        finalPrice = item['finalPrice']
        cityName = item['cityName']
        districtName = item['districtName']
        unitSummeries = item['unitSummeries']

        zhengtao = ''
        buju = ''
        pingfeng = 0.0
        dianping = 0
        for unit in unitSummeries:
            if '整套' in unit['text']:
                zhengtao = unit['text']
            elif '床' in unit['text']:
                buju = unit['text']
            elif '分' in unit['text']:
                _pingjia = unit['text'].split('/')
                pingfeng = float(_pingjia[0].replace('分', ''))
                dianping = int(_pingjia[1].replace('点评', ''))

        List = [unitId, totalCount, unitName, longitude, latitude, address, unitInfor,
                productPrice, finalPrice, cityName, districtName, zhengtao, buju, pingfeng, dianping]
        with open(filename, 'a', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow(List)
            print(List)
