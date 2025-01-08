from abc import ABC

from db.DBProperty import DBProperty
from db.DBType import DBType


class ChromaDBProperty(DBProperty, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(DBType.CHROMA)
        self.args = args
        self.kwargs = kwargs

    def connectionInfo(self) -> (str, int):
        host = self.kwargs['host']  # 키가 없으면 KeyError 발생
        port = self.kwargs['port']  # 필수

        return host, port
