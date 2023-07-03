import datetime
import random
import uuid
from time import sleep

import backoff
from confluent_kafka.cimpl import Producer, Consumer

from config import config, backoff_settings
from etl_logger import etl_logger

producer = Producer({"bootstrap.servers": config.kafka_host})


class Event:
    def __init__(self, user_id, movie_id, timestamp_of_film):
        self.user_id = user_id
        self.movie_id = movie_id
        self.timestamp_of_film = timestamp_of_film


kafka_config = {
    "bootstrap.servers": config.kafka_host,
    "group.id": 'timestamp-of-film',
    "auto.offset.reset": "smallest",
}

consumer = Consumer(kafka_config)


@backoff.on_exception(**backoff_settings)
def extract_from_kafka():
    """Выгрузить события из Kafka"""
    events = []
    consumer.subscribe(['movies_views'])
    messages = consumer.consume(num_messages=50, timeout=1.0)
    for message in messages:
        info_str = str(message.key(), 'utf-8') + ' ' + str(message.value(), 'utf-8')
        etl_logger.info(info_str)
        person_uuid, film_uuid = str(message.key(), 'utf-8').split('+')
        events.append(Event(person_uuid, film_uuid, str(message.value(), 'utf-8')))

    return events


def fill_random_kafka():
    """Заполнить Kafka тестовыми событиями"""
    for i in range(random.randint(0, 10)):
        producer.produce(topic='movies_views',
                         value=str(datetime.datetime.utcnow()),
                         key=str(uuid.uuid4()) + '+' + str(uuid.uuid4()))
    producer.flush()

    sleep(1)
