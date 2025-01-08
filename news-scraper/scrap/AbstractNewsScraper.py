import http.client
from abc import ABC, abstractmethod
from typing import List, Any

from scrap.NewsItemContainer import NewsItemContainer
from scrap.NewsType import NewsType


class AbstractNewsScraper(ABC):
    def __init__(self, news_type: NewsType):
        # 스크랩 한 뉴스의 타입을 말함
        self.news_type = news_type
        self.scrap_news: List[Any] = list()

    @abstractmethod
    def fetch_news(self, query: str) -> NewsItemContainer:
        pass

    @abstractmethod
    def parse_response(self, response: List[Any]) -> List[Any]:
        pass

    @abstractmethod
    def getScrapedNews(self) -> List[Any]:
        pass
