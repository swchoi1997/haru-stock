from abc import ABC

from pymongo import MongoClient

from db.AbstractDBObj import AbstractDBObj
from db.DBProperty import DBProperty


class MongoDbObj(AbstractDBObj, ABC):
    def __init__(self, db_property: DBProperty):
        super().__init__(db_property)
        self.default_dbs = None

    def connect(self) -> MongoClient:
        if self.connection is not None:
            return self.connection

        uri: str = self.db_property.connectionInfo()

        self.connection: MongoClient = MongoClient(uri)
        #기본 데이터베이스 설정
        self.default_dbs = self.connection.get_default_database()

        return self.connection

    def disconnect(self) -> None:
        if self.connection is not None:
            return
        conn: MongoClient = self.connection
        conn.close()

    def getConnection(self) -> MongoClient:
        return self.connection




# if __name__ == '__main__':
    # property = MongoDBProperty(
    #     host=['haru-stock-mongo-master', 'haru-stock-mongo-replica1', 'haru-stock-mongo-replica2'],
    #     port=[27027, 27028, 27029],
    #     user='haru',
    #     passwd='haru',
    #     db='haru_stock')

    # property = MongoDBProperty(
    #     host='127.0.0.1',
    #     port=27027,
    #     user='haru',
    #     passwd='haru',
    #     db='haru_stock')
    # obj = MongoDbObj(property)
    # mongo = obj.connect()
    # dbs = mongo.get_default_database()
    #
    # collection = dbs["g2"]
    # collection.insert_many([
    #     {"name": "Alice", "age": 25, "city": "Seoul"},
    #     {"name": "Bob", "age": 30, "city": "Busan"},
    #     {"name": "Charlie", "age": 35, "city": "Incheon"},
    # ])
    #
    # for d in collection.find():
    #     print(d)

    # ReplicaSet URI
    # uri = "mongodb://haru:haru@localhost:27027/haru_stock?directConnection=true"
    # client = MongoClient(uri)
    # db = client["haru_stock"]
    #
    # db_list = client.list_database_names()
    # client.get_default_database()
    # client.get_default_database()
    # print(client.get_default_database())
    #
    # #
    # # # 데이터 작업
    # collection = db["test"]
    # collection.insert_many()
    # collection.insert_one({"message": "Hello from ReplicaSet!"})
    # # print("Data inserted into ReplicaSet.")
    #
    # # 연결 종료
    # client.close()
    #
    # i= 0

