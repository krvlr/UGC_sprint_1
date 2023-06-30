import logging

logging.basicConfig()
etl_logger = logging.getLogger("ETL_KAFKA_TO_CLICKHOUSE")
etl_logger.setLevel(level=logging.INFO)
