import json
from queue import Queue
from typing import Dict, Any

import confluent_kafka

from MessageBridge.MessageBridge import MessageProducer


class KafkaProducer(MessageProducer):
    def __init__(
            self,
            kafka_config: dict,
            topic: str,
            process_message_callback,
            outer_queue: Queue[Dict[Any, Any]]
    ):
        """
        Kafka 메시지를 보내는 클래스 초기화

        :param kafka_config: Kafka Consumer 설정
        :param topic: 구독할 Kafka 토픽
        :param process_message_callback: 메세지 보낸 후 처리 함수
        :param outer_queue: 외부로 보낼 메세지를 담은 queue
        """
        self.kafka_config = kafka_config
        self.topic = topic
        self.outer_queue = outer_queue
        self.process_message_callback = process_message_callback,
        self.producer = confluent_kafka.Producer(self.kafka_config)

    def produce(self, is_running):
        try:
            while is_running:
                outer_msg = self.outer_queue.get()
                if outer_msg is None:
                    continue

                # 딕셔너리가 아니면 잘못된 메세지 전달한것으로 판단
                if not isinstance(outer_msg, dict):
                    raise TypeError

                kafka_msg = json.dumps(outer_msg).encode("utf-8")
                self.producer.produce(
                    topic=self.topic,
                    key=None,
                    value=kafka_msg,
                    callback=self.process_message_callback
                )
                self.producer.poll(0)

        except Exception as e:
            print(f"KafkaProducer produce 에러: {e}")

            # TODO alert
        finally:
            self.producer.flush()