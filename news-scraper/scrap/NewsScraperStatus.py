from enum import Enum


class NewsScraperStatus(Enum):
    READY = "READY"
    SCRAPING = "SCRAPING"
    VECTORING = "VECTORING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

