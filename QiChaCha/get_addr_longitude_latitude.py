import requests
from urllib.parse import quote
import json


def get_addr_longitude_latitude(keyword):
    url = "https://ditu.amap.com/service/poiInfo?query_type=TQUERY&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=12&keywords={}".format(
        quote(keyword))

    payload = {}
    headers = {}
    try:
        with requests.request("GET", url, headers=headers, data=payload) as response:
            js = json.loads(response.text)
            target = js['data']['poi_list'][0]
            try:
                if target['address']:
                    address = target['address']
                else:
                    address = keyword
            except Exception as e:
                address = keyword
            L = [
                address,
                target['longitude'],
                target['latitude']
            ]

    except Exception as e:
        L = ['', '', '']

    return L


if __name__ == "__main__":
    L = get_addr_longitude_latitude('上海市嘉定区真新街道金沙江路3131号4幢中区123室')
    print(L)
