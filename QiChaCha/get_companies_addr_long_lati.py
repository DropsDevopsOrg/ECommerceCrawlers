import csv
import pandas as pd
from get_addr_longitude_latitude import get_addr_longitude_latitude
import threading
import time
import os

if not os.path.exists('./csv/全国工业园区企业简要信息_addr.csv'):
    header = ['province', 'city', 'county', 'park', 'parkaddr', 'parkxy', 'parkx', 'parky', 'area', 'numcop', 'company',
              'person', 'capital', 'settime', 'email', 'phone', 'address', 'addressxy', 'addressx', 'addressy', 'state', 'url']
    with open('./csv/全国工业园区企业简要信息_addr.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

file_name = './csv/去重_全国工业园区企业简要信息.csv'

csv_data = pd.read_csv(file_name)
csv_data_ori = pd.read_csv('./csv/全国工业园区信息_addr.csv')
length = len(csv_data)
length_ori = len(csv_data_ori)
print(length, length_ori)
# csv_data['parkaddr'] = ''
# csv_data['parkxy'] = ''
# csv_data['parkx'] = ''
# csv_data['parky'] = ''
# csv_data['addressxy'] = ''
# csv_data['addressx'] = ''
# csv_data['addressy'] = ''


t_start = time.time()
ListTask = []
for i in range(length):
    ListTask.append(i)


def thread_task():
    try:
        while True:
            num = ListTask.pop(0)
            park = csv_data.loc[num, 'park']
            for i in range(length_ori):
                if csv_data_ori.loc[i, 'park'] == park:
                    parkaddr = csv_data_ori.loc[i, 'parkaddr']
                    parkxy = csv_data_ori.loc[i, 'parkxy']
                    parkx = csv_data_ori.loc[i, 'parkx']
                    parky = csv_data_ori.loc[i, 'parky']
                    break
            address = csv_data.loc[num, 'address']
            company = csv_data.loc[num, 'company']
            # print(address, company)
            for i in range(5):
                L = get_addr_longitude_latitude(address)
                if L != ['', '', '']:
                    addressx = L[1]
                    addressy = L[2]
                    addressxy = L[1]+','+L[2]
                    print('已完成:\t{} / {}    {}    {}'.format(num, length, company, L))
                    break
                elif i == 4:
                    addressx = ''
                    addressy = ''
                    addressxy = ','
                    print('\t无数据:\t{} / {}    {}    {}'.format(num, length, company, L))
                else:
                    time.sleep(0.1)
            # print(2)
            # province,city,county,park,area,numcop,company,person,capital,settime,email,phone,address,state,url
            List = [
                csv_data.loc[num, 'province'],
                csv_data.loc[num, 'city'],
                csv_data.loc[num, 'county'],
                csv_data.loc[num, 'park'],
                parkaddr,
                parkxy,
                parkx,
                parky,
                csv_data.loc[num, 'area'],
                csv_data.loc[num, 'numcop'],
                csv_data.loc[num, 'company'],
                csv_data.loc[num, 'person'],
                csv_data.loc[num, 'capital'],
                csv_data.loc[num, 'settime'],
                csv_data.loc[num, 'email'],
                csv_data.loc[num, 'phone'],
                csv_data.loc[num, 'address'],
                addressxy,
                addressx,
                addressy,
                csv_data.loc[num, 'state'],
                csv_data.loc[num, 'url']
            ]
            # print(List)
            with open('./csv/全国工业园区企业简要信息_addr.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(List)

    except Exception as e:
        pass


threads = []
for i in range(80):
    thread = threading.Thread(target=thread_task, args=())
    threads.append(thread)

# 启动多线程
for t in threads:
    t.start()
    print('开启线程:\t'+t.name)

for t in threads:
    t.join()
    print('关闭线程:\t'+t.name)

t_end = time.time()
print('\n运行时间:', t_end-t_start)
