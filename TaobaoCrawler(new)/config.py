# 搜索配置
# 搜索内容
str_searchContent = 'iPhone Xs'
# 每页显示数量
num_pageSize = 100
# 从第一页 至 第几页（理论上可穷尽阿里服务器），推荐填入 1~100 ，页数再大则显示的内容匹配度不足
num_page = 2
# 阿里服务编号，12574478 固定不要更改，如菜鸟裹裹为 12574478 固定
appKey = '12574478'  # 不要更改！！！

###########################################
# 爬取内容设置

# 开启线程数
threads_num_get_pages = 1  # 抓取搜素页的线程数, 默认为 1
threads_num_get_comments = 3  # 抓取评论页的线程数,当为 0 时,不抓取详情页面(评论)

###########################################
# 储存
switch_save = 0  # 本地 csv 存储
# switch_save = 1 # mysql 存储
# switch_save = 2 # mysql + redis 存储

# redis
redis_host = '127.0.0.1'
redis_port = 6379

# mysql
mysql_host = '127.0.0.1'
mysql_port = 3306
mysql_user = 'root'
mysql_passwd = '123456'
mysql_db = 'taobao'
mysql_charset = 'utf8'

###########################################
# 代理设置
# 隧道服务器
_tunnel_host = "tps189.kdlapi.com"
_tunnel_port = "15818"

# 隧道用户名密码
_tid = "t17888082960619"
_password = "gid72p4o"

proxies = {
    "http": "http://%s:%s@%s:%s/" % (_tid, _password, _tunnel_host, _tunnel_port),
    "https": "https://%s:%s@%s:%s/" % (_tid, _password, _tunnel_host, _tunnel_port)
}

###########################################
