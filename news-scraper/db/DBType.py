from enum import Enum


class DBType(Enum):
    MYSQL = "MYSQL"
    POSTGRESQL = "POSTGRESQL"
    MONGO = "MONGO"
    CHROMA = "CHROMA"


