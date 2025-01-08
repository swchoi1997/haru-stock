import urllib.parse
from typing import Dict, Any

from config.NcpParams import NcpParams


class NcpNewsParams(NcpParams):
    def __init__(
            self,
            query: str,
            start: int,
            display: int = 100,
            sort: str = "date"
    ):
        """
        :param query: 검색어, UTF-8 Encoding
        :param start: 검색 시작 위치(기본값 1, 최댓값 1000)
        :param display: 한번에 표시될 검색 결과 개수(기본값 10, 최댓값 100)
        :param sort: 검색 결과 정렬방법,
                    - sim: 정확도순으로 내림차순 정렬(기본값)
                    - date: 날짜순으로 내림차순 정렬
        """
        self._query = query  # URL 인코딩되어 UTF-8 형식으로 변환됩니다.
        self._start = start
        self._display = display
        self._sort = sort

    def get_param_map(self) -> Dict[str, Any]:
        # __dict__에서 변수명 정리 (맹글링된 이름 복원)
        return {
            key.replace(f"_", ""): value for key, value in self.__dict__.items()
        }
