from abc import ABC

import chromadb
from chromadb import ClientAPI

from db.AbstractDBObj import AbstractDBObj
from db.DBProperty import DBProperty
from db.chroma.ChromaDBProperty import ChromaDBProperty


class ChromaDbObj(AbstractDBObj, ABC):

    def __init__(self, db_property: ChromaDBProperty):
        super().__init__(db_property)

    def getDBProperty(self):
        return super().getDBProperty()

    def connect(self) -> ClientAPI:
        host, port = self.getDBProperty().connectionInfo()
        self.connection = chromadb.HttpClient(host=host, port=port)

        return self.connection

    def IsConnect(self):
        try:
            self.connection.heartbeat()
            return True
        except Exception:
            return False

    def disconnect(self) -> None:
        # Http로 연결되는 무상태 구조라 close 메서드가 없음
        self.connection = None
