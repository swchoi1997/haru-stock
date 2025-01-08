import os
from datetime import datetime
from typing import List

import google.generativeai as genai
from langchain.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo import MongoClient

from db.AbstractDBObj import AbstractDBObj
from scrap.AbstractNewsScraper import AbstractNewsScraper
from scrap.NewsItemContainer import NewsItemContainer
from scrap.NewsScraperLog import NewsScraperLog
from scrap.NewsScraperStatus import NewsScraperStatus
from scrap.naver.NaverNewsItem import NaverNewsItem
from scrap.naver.NaverNewsScraperLog import NaverNewsScraperLog


class NewsScrap:
    """
    뉴스 스크랩을 수행하고, 원본 DB와 벡터 DB에 저장을 수행하는 클래스입니다.
    """
    def __init__(
            self,
            keyword: str,
            save_db: AbstractDBObj,
            vector_db: AbstractDBObj,
            scraper: AbstractNewsScraper,
            log: NewsScraperLog
    ):
        """
        NewsScrap 초기화 함수
        :param keyword: 뉴스 검색 키워드
        :param save_db: 뉴스 검색 원본 저장소
        :param vector_db: 뉴스 벡터 저장소
        :param scraper: 실제 newsScraper
        :param log: 실제 log
        """
        self.keyword = keyword
        self.save_db = save_db
        self.vector_db = vector_db
        self.scraper = scraper
        self.log: NaverNewsScraperLog = log

        if not self.save_db.IsConnect():
            self.save_db.connect()

    def run(self):
        conn: MongoClient = self.save_db.connection
        dbs = conn.get_default_database()
        collections = dbs['scrap_log']

        # 스크랩 시작 시간 & 상태 업데이트
        self.log.update_scrap_start_time(datetime.now())
        self.log.change_status(NewsScraperStatus.SCRAPING)
        self.upsert_log(collections)

        # 스크랩 시작
        result: NewsItemContainer = self.scraper.fetch_news(self.keyword)
        # DB 저장
        self.save_origin(result)

        # 스크랩 종료 시간 & 상태 업데이트
        self.log.update_scrap_end_time(datetime.now())
        self.log.update_scrap_count(len(result.news_item))

        # 성공 / 실패 여부 확인
        if result.result_msg != "":
            # "" 가 아니면 실패한거임
            self.log.change_status(NewsScraperStatus.FAILED)
            self.log.update_total_end_time(datetime.now())
            self.log.update_scrap_count(0)
            self.log.update_is_success(False)
            self.log.error_message = result.result_msg

            self.upsert_log(collections)

            return

        # 성공이라면 벡터링 시작
        self.log.change_status(NewsScraperStatus.VECTORING)
        self.log.update_vectoring_start_time(datetime.now())
        self.upsert_log(collections)

        # 벡터 DB 저장
        self.save_vector_db(result)

        # 벡터링 종료 시, 상태 종료
        self.log.update_total_end_time(datetime.now())
        self.log.update_vectoring_end_time(datetime.now())
        self.log.change_status(NewsScraperStatus.SUCCESS)
        self.log.update_is_success(True)

        self.upsert_log(collections)

        # DB 초기화
        self.save_db.disconnect()
        self.vector_db.disconnect()

    def upsert_log(self, collections):
        collections.update_one(
            {"_id": self.log.get_id()},  # 조건: _id가 같은 문서
            {"$set": self.log.to_dict()},  # 업데이트할 내용
            upsert=True  # 문서가 없으면 삽입
        )

    def save_origin(self, result: NewsItemContainer):
        db = self.save_db.connection

        dbs = db.get_default_database()
        collection = dbs[self.keyword]

        from pymongo.errors import BulkWriteError

        try:
            items: List[NaverNewsItem] = result.news_item
            collection.insert_many([item.to_dict() for item in items], ordered=False)


        except BulkWriteError as e:
            print(e.details)

    def save_vector_db(self, result: NewsItemContainer):
        if not self.vector_db.IsConnect():
            self.vector_db.connect()

        # Vector DB에 저장
        try:
            i = 0
            for news in result.news_item:
                print("Vector DB에 저장 : " + str(i))
                _id = news.getId()
                text = news.getDescription()
                pub_date = news.getPubDate()
                self.save_vector(_id, text, pub_date)
                i += 1
        except Exception as e:
            print(e)

    def save_vector(self, _id: str, text: str, pub_date: datetime):
        client = self.vector_db.connection

        from slugify import slugify
        slugify_keyword = slugify(self.keyword, lowercase=True)

        collection = client.get_or_create_collection(name=slugify_keyword)

        recursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100)

        doc = [Document(page_content=text, metadata={"id": _id, "date": pub_date})]

        chunks = recursiveCharacterTextSplitter.split_documents(doc)

        genai.configure(api_key=os.getenv("google_gemini_api_key"))

        for i, row in enumerate(chunks):
            doc_id = f"{row.metadata['id']}_{i}"
            print(doc_id, end="")
            existing_docs = collection.get(ids=[doc_id])

            if existing_docs and len(existing_docs["ids"]) > 0:
                print(" : " + str(existing_docs["ids"]))
                continue
            print()
            if len(row.page_content) <= 0:
                continue
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=row.page_content)

            embedding_vector = result["embedding"]

            collection.upsert(
                documents=[row.page_content],
                embeddings=[embedding_vector],
                # 고유 ID를 위해 uuid 사용 (원하시면 다른 방식을 써도 됨)
                ids=[doc_id],
                # 메타데이터에 원본 뉴스 ID 등을 넣어둠
                metadatas=[{
                    "original_id": row.metadata["id"],
                    "pub_date": row.metadata["date"].isoformat(),
                    "ref_count": 0
                }]
            )
