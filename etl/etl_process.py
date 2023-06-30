import logging
from time import sleep

from clickhouse_loader import create_clickhouse_db, bulk_save_to_clickhouse

from kafka_extractor import fill_kafka, load_from_kafka

logging.basicConfig()
logger = logging.getLogger("etl")
logger.setLevel(level=logging.INFO)


def run_etl():
    """Запуск процесса проверки и переноса записей"""
    fill_kafka()

    create_clickhouse_db()

    logger.info('Loading from kafka')
    events = load_from_kafka()
    logger.info('Saving to clickhouse')
    bulk_save_to_clickhouse(events)
    logger.info('Success, transferred %s events', str(len(events)))


def run_etl_process():
    """Запуск основного периодического процесса ETL"""
    while True:
        try:
            run_etl()
        except Exception as ex:
            logging.error('Exception what' + str(ex))
        sleep(5)


if __name__ == '__main__':
    run_etl_process()
    logger.info('ETL kafka to clickhouse success')
