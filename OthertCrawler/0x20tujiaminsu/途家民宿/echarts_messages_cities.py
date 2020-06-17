from pyecharts.charts import Bar
from pyecharts import options as opts
import pandas as pd
import csv

# nameList = ['beijing', 'shanghai', 'guangzhou', 'shenzhen', 'suzhou', 'chengdu', 'chongqing', 'xian', 'wuhan', 'xiamen', 'qingdao',
#             'wulumuqi', 'lasa']

nameList = []
totalNum = []
meanProductPrice = []
meanFinalPrice = []
meanStars = []
meanCommit = []

csv_data = pd.read_csv('./csv/各城市信息统计.csv')
length = len(csv_data)
for i in range(length):
    nameList.append(csv_data.loc[i, 'city'])
    totalNum.append(int(csv_data.loc[i, 'totalNum']))
    meanProductPrice.append(int(csv_data.loc[i, 'meanProductPrice']))
    meanFinalPrice.append(int(csv_data.loc[i, 'meanFinalPrice']))
    meanStars.append(csv_data.loc[i, 'meanStars'])
    meanCommit.append(csv_data.loc[i, 'meanCommit'])


def Bar_Cities() -> Bar:
    bar = (
        Bar()
        .add_xaxis(nameList)
        .add_yaxis('总数', totalNum)
        .add_yaxis('平均原价', meanProductPrice)
        .add_yaxis('平均现价', meanFinalPrice)
        .add_yaxis('平均评分', meanStars)
        .add_yaxis('平均评论', meanCommit)
        .set_global_opts(title_opts=opts.TitleOpts(title='13个抽样城市名宿信息分析'))
    )
    return bar


bar = Bar_Cities()
bar.render('./html/13个抽样城市名宿信息分析.html')
