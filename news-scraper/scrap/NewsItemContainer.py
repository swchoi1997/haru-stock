from typing import List, Generic, TypeVar

from scrap import NewsItem

T = TypeVar("T", bound=NewsItem)


class NewsItemContainer(Generic[T]):
    def __init__(self, news_item: List[T], result_msg):
        self.news_item = news_item
        self.result_msg = result_msg

