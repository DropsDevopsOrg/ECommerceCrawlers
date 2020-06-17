from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType
import pandas as pd
import csv
import json

nameList = ['beijing', 'shanghai', 'guangzhou', 'shenzhen', 'suzhou', 'chengdu', 'chongqing', 'xian', 'wuhan', 'xiamen', 'qingdao',
            'wulumuqi', 'lasa']
data = []
loc = {}

for name in nameList:
    csv_data = pd.read_csv('./csv/途家民宿_{}.csv'.format(name))
    length = len(csv_data)
    for i in range(length):
        title = csv_data.loc[i, '标题']
        finalPrice = csv_data.loc[i, '现价']
        lon = csv_data.loc[i, '经度']
        lat = csv_data.loc[i, '维度']
        if lon and lat:
            data.append([title, str(finalPrice)])
            loc.update({title: [float(lon), float(lat)]})

dat = [[i[0], int(i[1])] for i in data]
with open('./json/途家民宿_China.json', 'w', encoding='utf8') as f:
    json.dump(loc, f, ensure_ascii=False)


def Geo_Addr_China() -> Geo:
    c = (
        Geo()
        .add_schema(maptype='china')
        .add_coordinate_json('./json/途家民宿_China.json')
        .add(
            "全国13个抽样城市民宿",
            dat,
            is_selected=True,
            symbol_size=5,
            is_large=True,
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True, min_=0, max_=500),
            title_opts=opts.TitleOpts(
                title="全国13个抽样城市民宿地理价格分布图")
        )
    )
    return c


c = Geo_Addr_China()
c.render('./html/全国13个抽样城市民宿地理价格分布图.html')
