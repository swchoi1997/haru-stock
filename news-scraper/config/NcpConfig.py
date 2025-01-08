import os
import urllib.request

from config.NcpParams import NcpParams


class NcpProperties:
    def __init__(self):
        self._baseUrl: str = os.getenv("ncp_news_base_url")
        self._id: str = os.getenv("ncp_client_id")
        self._secret: str = os.getenv("ncp_client_secret")
        self._max_count: int = int(os.getenv("ncp_max_scrap_count"))
        self._date_format: str = os.getenv("ncp_news_date_format")

    def getBaseUrl(self) -> str:
        return self._baseUrl

    def getClientId(self) -> str:
        return self._id

    def getClientSecret(self) -> str:
        return self._secret

    def getMaxScrapCount(self) -> int:
        return self._max_count

    def getDateFormat(self) -> str:
        return self._date_format



class NcpConfig:
    def __init__(self):
        self.ncp_properties = NcpProperties()

    def getNcpRequest(self, params: NcpParams) -> urllib.request.Request:
        # URL 조립
        url: str = f"{self.ncp_properties.getBaseUrl()}?{params.get_query_str()}"

        # 요청 설정
        request: urllib.request.Request = urllib.request.Request(url)

        # 헤더 추가
        request.add_header("X-Naver-Client-Id", self.ncp_properties.getClientId())
        request.add_header("X-Naver-Client-Secret", self.ncp_properties.getClientSecret())

        return request
