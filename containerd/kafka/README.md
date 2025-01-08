## Kafka 에 Topic 추가하는 방법(with Cli)

```
kafka-topics.sh --create \
  --bootstrap-server {hostname}:{port} \
  --replication-factor 1 \
  --partitions 3 \
  --topic {topic_name}
```

옵션 설명
- --bootstrap-server: Kafka 브로커 주소.
- --replication-factor: 토픽 데이터의 복제본 수.
- --partitions: 파티션 개수.
- --topic: 생성할 토픽 이름.


## Kafka로 메세지 보내는 방법(with cli)
```
kafka-console-producer.sh --broker-list {hostname}:{port} --topic {topic_name}
```
