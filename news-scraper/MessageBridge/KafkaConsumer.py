import json
import time
from queue import Queue

import mmh3
from confluent_kafka import Consumer, KafkaException

from MessageBridge.MessageBridge import MessageConsumer


class KafkaConsumer(MessageConsumer):
    def __init__(
            self,
            kafka_config: dict,
            topic: str,
            task_type: str,
            process_message_callback,
            inner_queue: Queue):
        """
        Kafka 메시지를 읽는 클래스 초기화

        :param kafka_config: Kafka Consumer 설정
        :param topic: 구독할 Kafka 토픽
        :param task_type
        :param process_message_callback: 메시지 처리 콜백 함수
        :param inner_queue: 내부로 담을 메세지
        """
        self.kafka_config = kafka_config
        self.topic = topic
        self.task_type = task_type
        self.process_message_callback = process_message_callback
        self.inner_queue = inner_queue
        self.consumer = Consumer(self.kafka_config)

    def get_partition(self, num_partitions: int) -> int:
        """
        주어진 키와 파티션 수에 따라 할당될 파티션을 계산
        :param key: 파티션 키
        :param num_partitions: 토픽의 파티션 수
        :return: 할당된 파티션 번호
        """
        hash_value = mmh3.hash(self.task_type, signed=False)  # murmur2 해시 계산
        partition = hash_value % num_partitions
        return partition

    def consume(self, is_running):
        """
        Kafka 메시지 소비 실행
        """
        try:
            self.consumer.subscribe([self.topic])
            print(f"KafkaReader: Subscribed to topic {self.topic}")

            while is_running:
                try:
                    kafka_msg = self.consumer.poll(timeout=1.0)
                    if kafka_msg is None:  # 타임아웃
                        continue

                    if kafka_msg.error():
                        if kafka_msg.error().is_eof():
                            print(f"KafkaReader: End of partition reached {kafka_msg.topic()} [{kafka_msg.partition()}]")
                        else:
                            raise KafkaException(kafka_msg.error())
                        continue
                    # 메시지 처리 콜백 호출

                    task = json.loads(kafka_msg.value().decode('utf-8'))
                    task_type = task["task_type"]

                    if task_type != self.task_type:
                        print(kafka_msg)
                        continue

                    self.process_message_callback(self.inner_queue, task)
                    # self.consumer.commit(asynchronous=False)  # 동기 커밋
                except KafkaException as e:
                    print(f"KafkaReader: KafkaException: {e}")
                except Exception as e:
                    print(f"KafkaReader: Exception: {e}")
                finally:
                    pass
                    # time.sleep(0.1)  # 짧은 대기 시간으로 루프 제어
        finally:
            pass
        #     self.consumer.close()
        #     print("KafkaReader: Consumer closed.")

#
# # Kafka 설정
# kafka_settings = {
#     'bootstrap.servers': '127.0.0.1:20000,127.0.0.1:20001,127.0.0.1:20002',  # 브로커 리스트
#     'group.id': 'my_consumer_group',  # Consumer Group ID
#     'auto.offset.reset': 'earliest',  # 처음부터 읽기 시작
# }

# if __name__ == "__main__":
#     topic_nm = "my_test_topic"
#     kafka_reader = KafkaConsumer(kafka_settings, topic_nm, process_message)
#
#     # 스레드 생성 및 실행
#     kafka_thread = threading.Thread(target=run_kafka_reader, args=(kafka_reader,))
#     kafka_thread.start()
#
#     try:
#         while True:
#             time.sleep(1)  # 메인 스레드 유지
#     except KeyboardInterrupt:
#         print("Stopping Kafka reader...")
#         kafka_reader.stop()
#         kafka_thread.join()
