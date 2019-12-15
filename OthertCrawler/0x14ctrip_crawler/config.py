import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MYSQL_HOST = '10.63.2.199'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'ctrip'
MYSQL_USERNAME = 'xxx'
MYSQL_PASSWORD = 'xxxx/'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(MYSQL_USERNAME, MYSQL_PASSWORD,
                                                                               MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE)
print(BASE_PATH)