import csv
import pandas as pd

# 去重处理
csv_data = pd.read_csv('./csv/全国工业园区企业简要信息.csv')
print(csv_data.duplicated(), len(csv_data))
csv_data = csv_data.drop_duplicates()
print(csv_data.duplicated(), len(csv_data))

csv_data['index'] = range(csv_data.shape[0])
csv_data = csv_data.set_index('index')

# province,city,county,park,area,numcop,company,person,capital,settime,email,phone,address,state,url
# 排序
csv_data = csv_data.sort_values(['province', 'city', 'county', 'park', 'area',
                                 'numcop', 'capital', 'settime'], ascending=[1, 1, 1, 1, 0, 0, 0, 1])
print(csv_data, len(csv_data))
csv_data.to_csv('./csv/去重_全国工业园区企业简要信息.csv', index=None)
