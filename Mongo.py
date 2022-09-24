from pymongo import MongoClient


class mongo_db:
    from pymongo import MongoClient
    import pymongo

    def __init__(self, string_value, password):
        CONNECTION_STRING = string_value.replace('<password>', password)
        self.client = MongoClient(CONNECTION_STRING)
        self.db = None


    def initialise_db(self, name):
        self.db = self.client[name]

    def insert_data(self,collection , data):
        column = self.db[collection]
        if type(data)==list:
            print("Its a list")
            result = column.insert_many(data)
        else:
            print("Single entry")
            result = column.insert_one(data)

    def get_data(self, collection, query):
        col = self.db[collection]
        return col.find(query)
