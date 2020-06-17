from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType
import pandas as pd
import csv
import json

name_ch = '苏州'
name_eng = 'suzhou'


csv_data = pd.read_csv('./csv/途家民宿_{}.csv'.format(name_eng))
length = len(csv_data)
data = []
loc = {}
for i in range(length):
    name = csv_data.loc[i, '标题']
    finalPrice = csv_data.loc[i, '现价']
    lon = csv_data.loc[i, '经度']
    lat = csv_data.loc[i, '维度']
    if lon and lat:
        data.append([name, str(finalPrice)])
        loc.update({name: [float(lon), float(lat)]})

dat = [[i[0], int(i[1])] for i in data]

with open('./json/途家民宿_{}.json'.format(name_eng), 'w', encoding='utf8') as f:
    json.dump(loc, f, ensure_ascii=False)


def Geo_Addr_City() -> Geo:
    c = (
        Geo()
        .add_schema(maptype=name_ch)
        .add_coordinate_json('./json/途家民宿_{}.json'.format(name_eng))
        .add(
            "{}民宿".format(name_ch),
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
                title="{}民宿 TOP2500 地理价格分布图".format(name_ch))
        )
    )
    return c


c = Geo_Addr_City()
c.render('./html/地理价格_{}.html'.format(name_eng))
