import hashlib
from datetime import datetime
from enum import Enum
from typing import Dict

from scrap.NewsItem import NewsItem


class NewsKeys(Enum):
    TITLE = "title"
    LINK = "link"
    DESCRIPTION = "description"
    ORIGINAL_LINK = "originallink"
    PUB_DATE = "pubDate"


class NaverNewsItem(NewsItem):
    def __init__(
            self,
            _id: str,
            title: str,
            link: str,
            description: str,
            original_link: str,
            pub_date: datetime
    ):
        super().__init__(_id, title, link, description)
        self.original_link = original_link
        self.pub_date = pub_date

    @classmethod
    def from_dict(cls, data: Dict[str, str], date_format: str):
        """
        딕셔너리를 받아 NaverNewsItem 객체를 생성하는 클래스 메서드
        """
        unique_id = hashlib.md5(data.get(NewsKeys.TITLE.value).encode('utf-8')).hexdigest()

        return cls(
            _id=unique_id,
            title=data.get(NewsKeys.TITLE.value),
            link=data.get(NewsKeys.LINK.value),
            description=data.get(NewsKeys.DESCRIPTION.value),
            original_link=data.get(NewsKeys.ORIGINAL_LINK.value),
            pub_date=datetime.strptime(data.get(NewsKeys.PUB_DATE.value), date_format) if data.get(
                NewsKeys.PUB_DATE.value) else None
        )

    def to_dict(self):
        """
            NaverNewsItem 객체를 딕셔너리로 변환하는 메서드
            """
        return {
            "_id": self._id,  # 부모 클래스 속성 포함
            NewsKeys.TITLE.value: self.title,
            NewsKeys.LINK.value: self.link,
            NewsKeys.DESCRIPTION.value: self.description,
            NewsKeys.ORIGINAL_LINK.value: self.original_link,
            NewsKeys.PUB_DATE.value: self.pub_date.strftime('%Y-%m-%d %H:%M:%S') if self.pub_date else None
        }

    def getId(self) -> str:
        return self._id

    def getTitle(self):
        return self.title

    def getLink(self):
        return self.link

    def getDescription(self):
        return self.description

    def getOriginal_link(self):
        return self.original_link

    def getPubDate(self) -> datetime:
        return self.pub_date
