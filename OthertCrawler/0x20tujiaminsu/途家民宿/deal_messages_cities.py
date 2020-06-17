import pandas as pd
import csv

nameList = ['beijing', 'shanghai', 'guangzhou', 'shenzhen', 'suzhou', 'chengdu', 'chongqing', 'xian', 'wuhan', 'xiamen', 'qingdao',
            'wulumuqi', 'lasa']

# nameList = ['beijing']

with open('./csv/各城市信息统计.csv', 'a', newline='', encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerow(['city', 'totalNum', 'meanProductPrice',
                     'meanFinalPrice', 'meanStars', 'meanCommit'])

for name in nameList:
    csv_data = pd.read_csv('./csv/途家民宿_{}.csv'.format(name))
    length = len(csv_data)
    city = name
    totalNum = csv_data.loc[0, '总数']
    _mean = csv_data.mean()
    print(_mean)
    meanProductPrice = int(_mean['原价'])
    meanFinalPrice = int(_mean['现价'])
    meanStars = round(_mean['评分'], 2)
    meanCommit = round(_mean['点评'], 2)
    L = [city, totalNum, meanProductPrice,
         meanFinalPrice, meanStars, meanCommit]
    with open('./csv/各城市信息统计.csv', 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(L)
