

MAX_PAGE = 99

HEADERS = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/73.0.3683.86 Safari/537.36',
}

MONGO_IP = 'localhost'
MONGO_PORT = 27017

# 关键字
from dbkeyword import Mongo
keywordb = Mongo()
KEYWORD = keywordb.select({})

# 配置信息
from dbconfig import Mongo
configdb =Mongo()
CONFIG = configdb.select({"flag":1})

# 用户信息
from  dbuserinfo import Mongo
userinfodb = Mongo()
USERINFO = userinfodb.select({})
# cookie信息
from dbcookie import DbClient
cookiedb = DbClient()

# 商品信息
from  dbproduct import Mongo
productdb = Mongo()

# 相似商品
from dbsimil import Mongo
simildb = Mongo()

