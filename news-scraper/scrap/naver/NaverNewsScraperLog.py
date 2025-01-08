from datetime import datetime

from scrap.NewsScraperLog import NewsScraperLog
from scrap.NewsScraperStatus import NewsScraperStatus
from scrap.NewsType import NewsType


class NaverNewsScraperLog(NewsScraperLog):

    def __init__(
            self,
            status: NewsScraperStatus,
            keyword: str,
            total_start_time: datetime,
            total_end_time: datetime,
            is_success: bool,
            scrap_start_time: datetime,
            scrap_end_time: datetime,
            scrap_count: int,
            error_message: str = None
    ):
        """
        네이버 뉴스 스크래핑 작업 로그를 담는 엔티티 클래스

        :param status: 스크래핑 상태
        :param keyword: 스크래핑에 사용된 키워드
        :param total_start_time: 전체 스크래핑 작업 시작 시간
        :param total_end_time: 전체 스크래핑 작업 종료 시간
        :param is_success: 스크래핑 작업 성공 여부
        :param scrap_start_time: 실제 스크래핑 시작 시간
        :param scrap_end_time: 실제 스크래핑 종료 시간
        :param scrap_count: 스크래핑된 뉴스 기사 수
        """
        super().__init__(
            NewsType.NAVER,
            status,
            keyword,
            total_start_time,
            total_end_time,
            is_success
        )
        self.scrap_start_time = scrap_start_time  # 실제 스크래핑 시작 시간
        self.scrap_end_time = scrap_end_time  # 실제 스크래핑 종료 시간
        self.vectoring_start_time = None
        self.vectoring_end_time = None
        self.scrap_count = scrap_count  # 스크래핑된 뉴스 기사 수
        self.error_message = error_message  # 에러메세지

    @classmethod
    def init(cls, status: NewsScraperStatus, keyword: str) -> "NaverNewsScraperLog":
        """
        기본값을 미리 설정한 초기화 메서드.
        필요한 값만 받아서 NaverNewsScraperLog 객체를 생성합니다.

        :param status: 스크래핑 작업 상태
        :param keyword: 스크래핑 키워드
        :return: 초기화된 NaverNewsScraperLog 객체
        """
        return cls(
            status=status,
            keyword=keyword,
            total_start_time=datetime.now(),
            total_end_time=None,
            is_success=None,
            scrap_start_time=None,
            scrap_end_time=None,
            scrap_count=None,
        )

    def change_status(self, status: NewsScraperStatus):
        self.status = status

    def update_scrap_start_time(self, scrap_start_time: datetime):
        self.scrap_start_time = scrap_start_time

    def update_scrap_end_time(self, scrap_end_time: datetime):
        self.scrap_end_time = scrap_end_time

    def update_total_end_time(self, total_end_time: datetime):
        self.total_end_time = total_end_time

    def update_is_success(self, is_success: bool):
        self.is_success = is_success

    def update_scrap_count(self, scrap_count: int):
        self.scrap_count = scrap_count

    def update_error_message(self, error_message: str):
        self.error_message = error_message

    def update_vectoring_start_time(self, vectoring_start_time: datetime):
        self.vectoring_start_time = vectoring_start_time

    def update_vectoring_end_time(self, vectoring_end_time: datetime):
        self.vectoring_end_time = vectoring_end_time

    def to_dict(self) -> dict:
        result = self.__dict__.copy()
        result["news_type"] = self.news_type.value
        result["status"] = self.status.value
        # datetime 필드는 None이 아닐 때만 isoformat()으로 변환
        if self.total_start_time is not None:
            result["total_start_time"] = self.total_start_time.isoformat()

        if self.total_end_time is not None:
            result["total_end_time"] = self.total_end_time.isoformat()

        if self.scrap_start_time is not None:
            result["scrap_start_time"] = self.scrap_start_time.isoformat()

        if self.scrap_end_time is not None:
            result["scrap_end_time"] = self.scrap_end_time.isoformat()

        if self.vectoring_start_time is not None:
            result["vectoring_start_time"] = self.vectoring_start_time.isoformat()

        if self.vectoring_end_time is not None:
            result["vectoring_end_time"] = self.vectoring_end_time.isoformat()

        return result
