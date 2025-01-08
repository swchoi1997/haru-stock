import os
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from queue import Queue
from typing import Any

from MessageBridge.InnerQueueConsumer import InnerQueueConsumer
from MessageBridge.KafkaConsumer import KafkaConsumer
from MessageBridge.KafkaProducer import KafkaProducer
from db.chroma.ChromaDBProperty import ChromaDBProperty
from db.chroma.ChromaDbObj import ChromaDbObj
from db.mongo.MongoDBProperty import MongoDBProperty
from db.mongo.MongoDbObj import MongoDbObj
from scrap.NewsScraperStatus import NewsScraperStatus


# MongoDB 연결 함수
def connect_db():
    """
    MongoDB에 연결하여 MongoDbObj 객체를 반환합니다.
    환경 변수에서 MongoDB 연결 정보를 가져옵니다.
    """
    return MongoDbObj(MongoDBProperty(
        host=os.getenv("mongo_host"),
        port=os.getenv("mongo_port"),
        user=os.getenv("mongo_user"),
        passwd=os.getenv("mongo_password"),
        db=os.getenv("mongo_dbs")
    ))


# 벡터 데이터베이스 연결 함수
def connect_vector():
    """
    ChromaDB에 연결하여 ChromaDbObj 객체를 반환합니다.
    환경 변수에서 ChromaDB 연결 정보를 가져옵니다.
    """
    return ChromaDbObj(ChromaDBProperty(
        host=os.getenv("vector_host"),
        port=os.getenv("vector_port")
    ))


# Kafka 설정 로드 함수
def load_kafka_set(postfix: str) -> dict:
    """
    Kafka Consumer 설정을 로드하여 반환합니다.

    :param postfix: Consumer Group ID에 추가할 접미사 (각 Consumer를 구분하기 위해 사용)
    :return: (kafka_settings, kafka_topic, kafka_task_type)
    """
    kafka_settings = {
        'bootstrap.servers': os.getenv("kafka_hosts"),  # Kafka 브로커 주소
        'group.id': os.getenv("kafka_group_id") + "_" + postfix,  # Consumer Group ID
        'auto.offset.reset': os.getenv("kafka_task_offset")  # 처음부터 읽을지 최신부터 읽을지 설정
    }

    return kafka_settings


# 애플리케이션 관리 클래스
class AppManager:
    def __init__(self, app_name: str, worker_cnt: int = 2):
        """
        AppManager 초기화 함수

        :param app_name: 애플리케이션 이름 (Kafka Consumer Group을 구분하는 데 사용)
        :param worker_cnt: ThreadPoolExecutor의 최대 worker 수
        """
        self.app_name = app_name  # 애플리케이션 이름
        self.thread_pool = ThreadPoolExecutor(max_workers=worker_cnt)  # 스레드 풀 초기화
        self.is_running = False  # 애플리케이션 실행 상태 플래그
        self.db = connect_db()  # MongoDB 연결 객체
        self.vector = connect_vector()  # ChromaDB 연결 객체

        # Kafka 설정 로드
        self.kafka_set = load_kafka_set(self.app_name)
        self.kafka_receive_topic = os.getenv('kafka_receive_topic')
        self.kafka_receive_task_type = os.getenv('kafka_receive_task_type')

        self.kafka_send_topic = os.getenv('kafka_send_topic')
        self.kafka_send_task_type = os.getenv('kafka_send_task_type')

        self.inner_queue = Queue()  # 내부 메시지 큐 (Kafka 메시지를 처리할 때 사용)
        self.outer_queue = Queue()

        # 애플리케이션 실행 함수

    def run(self):
        """
        Kafka Consumer 및 InnerQueueConsumer를 실행하고,
        메시지를 처리하여 스레드 풀에 작업을 제출합니다.
        """

        # 스레드 풀에 작업을 제출하는 콜백 함수
        def on_inner_task_received_callback(message: Any):
            """
            Kafka에서 수신한 메시지를 받은 후 수행하는 콜백 함수

            :param message: Kafka에서 수신한 메시지
            """

            from NewsScraper import NewsScrap
            from scrap.naver.NaverNewsScraper import NaverNewsScraper
            from scrap.naver.NaverNewsScraperLog import NaverNewsScraperLog
            from pymongo import MongoClient

            # 몽고디비에, 시작 상태 로그 기록
            conn: MongoClient = connect_db().connect()
            dbs = conn.get_default_database()
            collections = dbs['scrap_log']

            scraper_log = NaverNewsScraperLog.init(status=NewsScraperStatus.READY, keyword=message['keyword'])
            collections.insert_one(scraper_log.to_dict())

            scrap = NewsScrap(keyword=message['keyword'],
                              save_db=self.db,
                              vector_db=self.vector,
                              scraper=NaverNewsScraper(),
                              log=scraper_log
                              )

            # 스레드 풀에서 작업 실행
            future = self.thread_pool.submit(scrap.run)

            # 작업 완료 후 결과 메시지를 outer_queue에 추가하는 콜백
            def on_task_done(fut):
                result_message = {
                    "keyword": message['keyword'],
                    "task_type": self.kafka_send_task_type,
                    "timestamp": time.time()
                }
                self.outer_queue.put(result_message)

            future.add_done_callback(on_task_done)

        def on_kafka_task_sent_callback(err, msg):
            """
            메시지 전송 완료 후 콜백 함수
            :param err: 에러 정보
            :param msg: 전송된 메시지에 대한 메타 정보
            """
            if err is not None:
                print(f"메시지 전송 실패: {err}")
                # TODO: 에러 로깅, 알림 등 필요 시 구현
            else:
                print(f"메시지 전송 성공: {msg.topic()} [{msg.partition()}] offset: {msg.offset()}")
            pass

        self.is_running = True  # 애플리케이션 실행 상태 설정

        # Kafka Consumer 생성
        kafka_consumer = KafkaConsumer(
            self.kafka_set, self.kafka_receive_topic, self.kafka_receive_task_type,
            process_message_callback=lambda inner_queue, message: inner_queue.put(message),
            inner_queue=self.inner_queue
        )

        kafka_producer = KafkaProducer(
            self.kafka_set, self.kafka_send_topic,
            process_message_callback=on_kafka_task_sent_callback,
            outer_queue=self.outer_queue
        )

        # 내부 큐에서 메시지를 소비하는 Consumer 생성
        inner_queue_consumer = InnerQueueConsumer(
            process_message_callback=on_inner_task_received_callback,  # 메시지 처리 콜백 함수
            inner_queue=self.inner_queue
        )

        # Kafka Consumer 및 InnerQueueConsumer를 스레드로 실행
        kafka_consumer = threading.Thread(target=kafka_consumer.consume, args=(self.is_running,))
        kafka_producer = threading.Thread(target=kafka_producer.produce, args=(self.is_running,))
        inner_queue_consumer = threading.Thread(target=inner_queue_consumer.consume, args=(self.is_running,))

        kafka_consumer.start()  # Kafka Consumer 스레드 시작
        kafka_producer.start()  # Kafka Producer 스레드 시작
        inner_queue_consumer.start()  # InnerQueueConsumer 스레드 시작

        # 애플리케이션 실행 상태를 지속적으로 확인
        while self.is_running:
            time.sleep(1)  # 1초 간격으로 상태 확인

    # 애플리케이션 중단 함수
    def interrupt(self):
        """
        애플리케이션 실행을 중단합니다.
        """
        self.is_running = False

    # 예외 처리 함수 (필요시 구현)
    def handle_exception(self, exception: Exception):
        """
        애플리케이션 실행 중 발생한 예외를 처리합니다.

        :param exception: 발생한 예외 객체
        """
        pass
