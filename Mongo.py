import bson
from pymongo import MongoClient


class mongo_db:
    from pymongo import MongoClient
    import pymongo

    def __init__(self, string_value, password, database_name):
        CONNECTION_STRING = string_value.replace('<password>', password)
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client[database_name]

    def create_collection(self, collection):
        self.db.create_collection(collection)
        return self.check_collection_present(collection)

    def check_collection_present(self, name):
        collections = self.db.list_collection_names()
        return name in collections

    def drop_collection(self, collection):
        column = self.db[collection]
        column.drop()
        return not self.check_collection_present(collection)

    def insert_data(self,collection , data):
        column = self.db[collection]
        if type(data)==list:
            print("Its a list")
            result = column.insert_many(data)
        else:
            print("Single entry")
            result = column.insert_one(data)

    def get_data(self, collection, filter):
        col = self.db[collection]
        return col.find(filter)
