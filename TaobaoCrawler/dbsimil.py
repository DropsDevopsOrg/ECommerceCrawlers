from pymongo import MongoClient, ASCENDING
from settings import MONGO_PORT, MONGO_IP


class Mongo():
    def __init__(self, ip=MONGO_IP, port=MONGO_PORT):
        conn = MongoClient(ip, port)
        self.db = conn.taobao
        self.collection = self.db.similproduct
        self.collection.create_index([('nid', ASCENDING)])

    def insert(self, item_dict):
        self.collection.insert_one(item_dict)

    def delete_all(self, query_dict):
        self.collection.delete_many(query_dict)

    def count(self):
        self.collection.count_documents({})
