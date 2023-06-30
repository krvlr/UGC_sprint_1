import datetime
import logging
import uuid
from time import sleep

from confluent_kafka.cimpl import Producer, Consumer

from config import config

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

logging.basicConfig()
logger = logging.getLogger("ETL")
logger.setLevel(level=logging.INFO)


def load_from_kafka():
    events = []
    consumer.subscribe(['movies_views'])
    messages = consumer.consume(num_messages=50, timeout=1.0)
    for message in messages:
        info_str = message.key() + message.value()
        logger.info(info_str)
        person_uuid, film_uuid = str(message.key()).split('+')
        events.append(Event(person_uuid, film_uuid, message.value()))

    return events


def fill_kafka():
    for i in range(4):
        producer.produce(topic='movies_views',
                         value=str(datetime.datetime.utcnow()),
                         key=str(uuid.uuid4()) + '+' + str(uuid.uuid4()))
    producer.flush()

    sleep(1)
