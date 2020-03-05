from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType
import pandas as pd
import csv
import json

csv_data = pd.read_csv("./csv/全国工业园区信息_addr.csv")
length = len(csv_data)
data = []
locations = []
for i in range(length):
    park = csv_data.loc[i, 'park']
    numcop = csv_data.loc[i, 'numcop']
    parkxy = csv_data.loc[i, 'parkxy']
    if ',' in str(parkxy):
        # str_ = '\n\n' + str(numcop)+'\n' + '测试'
        data.append([park, str(numcop)])    # 一定要写成字符串!!! 不然莫名其妙有bug, 针对pandas
        locations.append([park, parkxy])

dat = [[i[0], int(i[1])] for i in data]

loc = {}
for l in locations:
    park = l[0]
    x = float(l[1].split(',')[0])
    y = float(l[1].split(',')[1])
    loc.update({park: [x, y]})

with open('jn_parks.json', 'w', encoding='utf8')as f:
    json.dump(loc, f, ensure_ascii=False)


def bmap_visualmap_cities() -> Geo:
    c = (
        Geo()
        .add_schema(maptype="china")
        .add_coordinate_json('jn_parks.json')
        .add(
            "工业园区",
            dat,
            # "china",
            is_selected=True,
            symbol_size=5,
            is_large=True,
            progressive=4000
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True, min_=0, max_=100),
            title_opts=opts.TitleOpts(title="全国工业园区企业数量分布图")
        )
    )
    return c


c = bmap_visualmap_cities()
c.render('map.html')
