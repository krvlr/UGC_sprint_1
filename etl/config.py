from pydantic import BaseSettings, Field


class ETL_settings(BaseSettings):
    """ETL настройки"""
    kafka_host: str = Field('localhost:9092', env='KAFKA_HOST')
    clickhouse_host: str = Field('localhost', env='CLICKHOUSE_HOST')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = ETL_settings()
