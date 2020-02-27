import hashlib
# import time

# 0b7adbc3d337e9a469aa762944d2dbb6

h5_tk = 'e0c7d67a1c53c77c6b99713095604dd2'
t = '1582716745850'
appKey = '12574478'
data = '{"keyword":"华为手机","ppath":"","loc":"","minPrice":"","maxPrice":"","ismall":"","ship":"","itemAssurance":"","exchange7":"","custAssurance":"","b":"","clk1":"","pvoff":"","pageSize":"100","page":"","elemtid":"1","refpid":"","pid":"430673_1006","featureNames":"spGoldMedal,dsrDescribe,dsrDescribeGap,dsrService,dsrServiceGap,dsrDeliver, dsrDeliverGap","ac":"","wangwangid":"","catId":""}'


def sign():
    str = h5_tk+"&"+t+"&"+appKey+"&"+data
    m = hashlib.md5(str.encode(encoding='utf-8')).hexdigest()
    print(m)


if __name__ == "__main__":
    sign()
