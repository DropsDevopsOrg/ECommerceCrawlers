# 代理设置
# 隧道服务器
_tunnel_host = "tps172.kdlapi.com"
_tunnel_port = "15818"

# 隧道用户名密码
_tid = "t18288776426579"
_password = "ahiqf8pl"

proxies = {
    "http": "http://%s:%s@%s:%s/" % (_tid, _password, _tunnel_host, _tunnel_port),
    "https": "https://%s:%s@%s:%s/" % (_tid, _password, _tunnel_host, _tunnel_port)
}


# cookie 调出控制台，查询
_QCCSESSID = 'viajssfpmd8aohi8msai5a11p0'   # 可填入VIP账户 对应值
# 可用Postman 无cookie模拟请求，将返回的此值填入，有效期长达数月；用vip账户中的值也可，但易过期
_acw_tc = 'b683069715829049003957779e854980863847b379248edf39287f83c4'
cookie = 'acw_tc={}; QCCSESSID={}'.format(_acw_tc, _QCCSESSID)

parks_name = "全国工业园区信息"
companies_name = "全国工业园区企业简要信息"
