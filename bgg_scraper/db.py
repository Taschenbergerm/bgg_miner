import pymongo
from pymongo import MongoClient


class Connect(object):
    @staticmethod
    def get_connection():
        return MongoClient("mongodb://root:example@localhost:27017/")


def main():
    connection = Connect.get_connection()
    db = connection.test
    collection = db.test_collection
    collection.insert_one({"name": "John", "age": 30})

if __name__ == "__main__":
    main()