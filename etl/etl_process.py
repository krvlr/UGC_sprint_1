from time import sleep

import backoff

from clickhouse_loader import create_clickhouse_db, bulk_load_to_clickhouse
from config import backoff_settings
from etl_logger import etl_logger

from kafka_extractor import fill_random_kafka, extract_from_kafka


@backoff.on_exception(**backoff_settings)
def run_etl():
    """Запуск процесса проверки и переноса записей"""
    fill_random_kafka()

    create_clickhouse_db()

    etl_logger.info('Loading from kafka')
    events = extract_from_kafka()
    etl_logger.info('Saving to clickhouse')
    bulk_load_to_clickhouse(events)
    etl_logger.info('Success, transferred %s events', str(len(events)))


def run_etl_process():
    """Запуск основного периодического процесса ETL"""
    while True:
        try:
            run_etl()
        except Exception as ex:
            etl_logger.error('Exception what' + str(ex))
        sleep(10)


if __name__ == '__main__':
    run_etl_process()
    etl_logger.info('ETL kafka to clickhouse success')
