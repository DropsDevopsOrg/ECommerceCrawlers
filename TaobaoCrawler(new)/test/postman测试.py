import requests

url = "https://h5api.m.taobao.com/h5/mtop.alimama.union.sem.landing.pc.items/1.0/?jsv=2.4.0&appKey=12574478&t=1582716745850&sign=1b91fff529136fed287df8f0056cecd6&api=mtop.alimama.union.sem.landing.pc.items&v=1.0&AntiCreep=true&dataType=jsonp&type=jsonp&ecode=0&callback=mtopjsonp2&data=%7B%22keyword%22%3A%22%E5%8D%8E%E4%B8%BA%E6%89%8B%E6%9C%BA%22%2C%22ppath%22%3A%22%22%2C%22loc%22%3A%22%22%2C%22minPrice%22%3A%22%22%2C%22maxPrice%22%3A%22%22%2C%22ismall%22%3A%22%22%2C%22ship%22%3A%22%22%2C%22itemAssurance%22%3A%22%22%2C%22exchange7%22%3A%22%22%2C%22custAssurance%22%3A%22%22%2C%22b%22%3A%22%22%2C%22clk1%22%3A%22%22%2C%22pvoff%22%3A%22%22%2C%22pageSize%22%3A%22100%22%2C%22page%22%3A%22%22%2C%22elemtid%22%3A%221%22%2C%22refpid%22%3A%22%22%2C%22pid%22%3A%22430673_1006%22%2C%22featureNames%22%3A%22spGoldMedal%2CdsrDescribe%2CdsrDescribeGap%2CdsrService%2CdsrServiceGap%2CdsrDeliver%2C%20dsrDeliverGap%22%2C%22ac%22%3A%22%22%2C%22wangwangid%22%3A%22%22%2C%22catId%22%3A%22%22%7D"

payload = {}
headers = {
    'cookie': '_m_h5_tk=e0c7d67a1c53c77c6b99713095604dd2_1582728834870; _m_h5_tk_enc=4dd920929127292a2f2249db13ad10c4'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
