# 代理设置
# 隧道服务器
_tunnel_host = "tps176.kdlapi.com"
_tunnel_port = "15818"

# 隧道用户名密码
_tid = "t1828877642****"
_password = "ahiq****"

proxies = {
    "http": "http://%s:%s@%s:%s/" % (_tid, _password, _tunnel_host, _tunnel_port),
    "https": "https://%s:%s@%s:%s/" % (_tid, _password, _tunnel_host, _tunnel_port)
}


# cookie 调出控制台，查询
_QCCSESSID = 'uk6af3muj8g8g1uuqcbkbe****'   # 可填入VIP账户 对应值
# 可用Postman 无cookie模拟请求，将返回的此值填入，有效期长达数月；用vip账户中的值也可，但易过期
_acw_tc = 'b683069c15828674987773524e9e4d2fa9b5f0e6ff46ea41ab3801****'
cookie = 'acw_tc={}; QCCSESSID={}'.format(_acw_tc, _QCCSESSID)

parks_name = "全国工业园区信息"
companies_name = "全国工业区企业简要信息"
