import uuid
import time
from abc import ABC, abstractmethod
from datetime import datetime

from scrap.NewsScraperStatus import NewsScraperStatus
from scrap.NewsType import NewsType


class NewsScraperLog(ABC):
    def __init__(
            self,
            news_type: NewsType,
            status: NewsScraperStatus,
            keyword: str,
            total_start_time: datetime,
            total_end_time: datetime,
            is_success: bool):

        self._id = str(uuid.uuid4())
        self.keyword = keyword
        self.status = status
        self.news_type = news_type
        self.total_start_time = total_start_time
        self.total_end_time = total_end_time
        self.is_success = is_success

    def get_id(self) -> str:
        return self._id

    @abstractmethod
    def to_dict(self):
        pass

