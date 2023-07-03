import logging

import backoff
from pydantic import BaseSettings, Field


class ETL_settings(BaseSettings):
    """ETL настройки"""
    kafka_host: str = Field('localhost:9092', env='KAFKA_HOST')
    clickhouse_host: str = Field('localhost', env='CLICKHOUSE_HOST')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def backoff_hdlr(details):
    logging.warning("Backing off {wait:0.1f} seconds after {tries} tries "
                    "calling function {target} with args {args} and kwargs "
                    "{kwargs}".format(**details))


backoff_settings = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "max_tries": 20,
    'max_time': 30,
    'jitter': None,
    'on_backoff': backoff_hdlr
}

config = ETL_settings()
