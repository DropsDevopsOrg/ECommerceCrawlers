import csv
import pandas as pd
from get_addr_longitude_latitude import get_addr_longitude_latitude
import threading
import time

file_name = './csv/全国工业园区信息.csv'

csv_data = pd.read_csv(file_name)
length = len(csv_data)
print(length)
csv_data['parkaddr'] = ''
csv_data['parkxy'] = ''
csv_data['parkx'] = ''
csv_data['parky'] = ''

t_start = time.time()
ListTask = []
for i in range(length):
    ListTask.append(i)


def get_L(num, i, keyword):
    L = get_addr_longitude_latitude(keyword)
    if L != ['', '', '']:
        csv_data.loc[num, 'parkaddr'] = L[0]
        csv_data.loc[num, 'parkx'] = L[1]
        csv_data.loc[num, 'parky'] = L[2]
        csv_data.loc[num, 'parkxy'] = L[1]+','+L[2]
        print('已完成:\t{} / {}    {}    {}'.format(num, length, keyword, L))
        return 'break'
    elif i == 4:
        print('\t无数据:\t{} / {}    {}    {}'.format(num, length, keyword, L))
        return 'again'
    else:
        time.sleep(0.1)


def thread_task():
    try:
        while True:
            num = ListTask.pop(0)
            park = csv_data.loc[num, 'park']
            keyword = csv_data.loc[num, 'province'] + \
                csv_data.loc[num, 'city']+park
            for i in range(5):
                flag = get_L(num, i, keyword)
                if flag == 'break':
                    break
                elif flag == 'again':
                    sign = get_L(num, i, park)
                    if sign == 'break':
                        break
                    elif sign == 'again':
                        pass

    except Exception as e:
        pass


threads = []
for i in range(40):
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

csv_data.to_csv('./csv/全国工业园区信息_addr.csv', index=None)
