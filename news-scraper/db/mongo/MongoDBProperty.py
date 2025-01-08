from abc import ABC

from db.DBProperty import DBProperty
from db.DBType import DBType


class MongoDBProperty(DBProperty, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(DBType.MONGO)
        self.args = args
        self.kwargs = kwargs
        self.uri = self._build_uri()

    def _build_uri(self) -> str:
        """
        전달된 키워드 인자를 기반으로 MongoDB URI 생성
        """
        try:
            host = self.kwargs['host']  # 키가 없으면 KeyError 발생
            port = self.kwargs['port']  # 필수
            user = self.kwargs['user']  # 필수
            passwd = self.kwargs['passwd']  # 필수
            db = self.kwargs['db']  # 필수

            # 인증 정보 포함
            uri = f"mongodb://{user}:{passwd}@{host}:{port}/{db}?directConnection=true"

            if isinstance(host, list) and isinstance(port, list):
                if len(host) != len(port):
                    raise ValueError("host와 port 리스트의 길이가 일치해야 합니다.")
                # replica set URI 생성
                host_port_pairs = ",".join(f"{h}:{p}" for h, p in zip(host, port))
                return f"mongodb://{user}:{passwd}@{host_port_pairs}/{db}?replicaSet=dbrs"

            # 단일 호스트 URI 생성
            return f"mongodb://{user}:{passwd}@{host}:{port}/{db}?directConnection=true"


        except KeyError as e:
            raise ValueError(f"Required key '{e.args[0]}' is missing in kwargs.") from e

    def connectionInfo(self) -> str:
        return self.uri
