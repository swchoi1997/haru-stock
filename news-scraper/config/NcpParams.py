import urllib.parse
from typing import Dict, Any
from abc import ABC, abstractmethod

class NcpParams(ABC):

    @abstractmethod
    def get_param_map(self) -> Dict[str, Any]:
        pass

    def get_query_str(self) -> str:
        return urllib.parse.urlencode(self.get_param_map())

