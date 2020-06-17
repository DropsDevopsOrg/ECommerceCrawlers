import requests
from config import *


def getItems(city, pageIndex):
    try:
        url = "https://www.tujia.com/bingo/pc/search/searchhouse"

        _payload = '{"conditions":[{"type":1,"value":"_city"},{"label":"入住日期","type":2,"value":"2020-06-20"},{"label":"离店日期","type":3,"value":"2020-06-24"}],"defaultKeyword":"","onlyReturnTotalCount":false,"pageIndex":_pageIndex,"pageSize":49,"returnFilterConditions":true,"returnGeoConditions":true,"url":""}'
        payload = _payload.replace('_city', city).replace(
            '_pageIndex', str(pageIndex))
        headers = {
            'Content-Type': 'text/plain'
        }
        response = requests.request(
            "GET", url, headers=headers, data=payload.encode('utf8'), proxies=proxies)
        jsn = response.json()['data']
        items = jsn['items']
        totalCount = jsn['totalCount']
        return totalCount, items
    except Exception as e:
        print('\t地址请求错误!!')
        return 0, []


if __name__ == "__main__":
    print(getItems('shanghai', 61))
