from pymongo import MongoClient

from cookiepool.settings import MONGO_PORT, MONGO_IP

class DbClient():
    def __init__(self, ip=MONGO_IP, port=MONGO_PORT):
        conn = MongoClient(ip, port)
        self.db = conn.taobao
        self.cookie_set = self.db.cookies

    def insert(self, cookies):
        """
        Insert cookies to collection.
        :cookie: dict of cookies
        """
        self.cookie_set.insert_one(cookies)

    def delete_all(self,dict):
        self.cookie_set.delete_many(dict)

    def delete(self,user):
        """
        Delete cookies.
        """
        self.cookie_set.delete_one({"user":user})
    def update_cookie_flag2(self,user):

        self.cookie_set.update({'user':user},{'$set':{"flag":2}})
    def update_cookie_flag0(self,user):
        self.cookie_set.update({'user':user},{'$set':{"flag":0}})
    def update_cookie_flag1(self,user,cookies,t):
        self.cookie_set.update({'user':user},{'$set':{"flag":1,"cookies":cookies,"time":t}})
    def get_cookies(self,flag):
        """
        Get cookies
        :return: if cookies exist, return cookie, else return None
        """
        q = self.cookie_set.find_one({"flag":flag})
        if q:
            return q
        else:
            return None

    def get_requests_cookie(self):
        q = self.cookie_set.find_one({"flag":1})
        d = {}
        if q:
            cookies = q['cookies']
            for cookie in cookies:
                d[cookie.get('name')] = cookie.get('value')
            return d
        else:
            return None


