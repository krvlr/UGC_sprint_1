import datetime
import json
import uuid
from time import sleep
import logging
from clickhouse_driver import Client
from confluent_kafka.cimpl import Producer
from pydantic import BaseModel
from settings import test_base_settings

producer = Producer(
    {"bootstrap.servers": f"{test_base_settings.kafka_host}:{test_base_settings.kafka_port}"})

clickhouse_client = Client(
    host=test_base_settings.clickhouse_host,
    alt_hosts="clickhouse-node2, clickhouse-node3, clickhouse-node4",
)


class FilmProgress(BaseModel):
    user_id: str
    movie_id: str
    timestamp_of_film: str


def fill_random_kafka():
    """Заполнить Kafka тестовыми событиями"""
    for i in range(100):
        f = FilmProgress(user_id=str(uuid.uuid4()),
                         movie_id=str(uuid.uuid4()),
                         timestamp_of_film=str(datetime.datetime.utcnow()))
        event = f.dict()
        key = event["user_id"] + event["movie_id"]
        producer.produce(topic='movies_views',
                         value=json.dumps(event).encode("utf-8"),
                         key=key)
    producer.flush()
    sleep(1)


def get_events_from_clickhouse():
    events = clickhouse_client.execute(
        """
        SELECT * FROM movies_events.regular_table
        """)
    return events


def clear_clickhouse():
    clickhouse_client.execute(
        """
        TRUNCATE TABLE IF EXISTS movies_events.regular_table
        """)


def test_kafka_to_clickhouse():
    clear_clickhouse()
    fill_random_kafka()
    events_size = 0
    count_of_attempts = 0
    while events_size != 100 and count_of_attempts < 5:
        events = get_events_from_clickhouse()
        events_size = len(events)
        count_of_attempts += 1
        sleep(3)
    assert (events_size == 100)
    assert (count_of_attempts < 5)
