from abc import ABC, abstractmethod
from datetime import datetime

class NewsItem(ABC):
    def __init__(self, _id: str, title: str, link: str, description: str):
        """
        뉴스 데이터를 담는 클래스.
        """
        self._id = _id
        self.title = title
        self.link = link
        self.description = description

    @abstractmethod
    def to_dict(self):
        pass





