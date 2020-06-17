# 代理设置
# 隧道服务器
_tunnel_host = "tps163.kdlapi.com"
_tunnel_port = "15818"

# 隧道用户名密码
_tid = "t18419733285353"
_password = "a3kklbuw"

proxies = {
    "http": "http://%s:%s@%s:%s/" % (_tid, _password, _tunnel_host, _tunnel_port),
    "https": "https://%s:%s@%s:%s/" % (_tid, _password, _tunnel_host, _tunnel_port)
}
