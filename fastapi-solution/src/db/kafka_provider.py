from typing import Optional

from db.base_db import QueueProvider
from kafka import KafkaProducer

# from aiokafka import AIOKafkaProducer
import json


kafka_producer: Optional[KafkaProducer] = None


class KafkaQueueProvider(QueueProvider):
    def __init__(self, kafka_producer: KafkaProducer):
        self.kafka_producer = kafka_producer

    def send(self, topic, event, key):
        self.kafka_producer.send(
            topic=topic, value=json.dumps(event).encode("utf-8"), key=key.encode("utf-8")
        )


# @lru_cache()
async def get_kafka_queue_provider() -> KafkaProducer:
    return KafkaQueueProvider(kafka_producer=kafka_producer)
