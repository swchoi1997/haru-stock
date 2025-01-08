from abc import abstractmethod

from db.DBProperty import DBProperty


class AbstractDBObj:
    def __init__(self, db_property: DBProperty):
        self.connection = None
        self.db_property = db_property

    def getDBProperty(self):
        return self.db_property

    @abstractmethod
    def connect(self):
        pass

    def IsConnect(self):
        return self.connection is not None

    @abstractmethod
    def disconnect(self) -> None:
        pass
