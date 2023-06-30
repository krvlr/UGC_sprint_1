import backoff
from clickhouse_driver import Client

from config import config, backoff_settings

clickhouse_client = Client(
    host=config.clickhouse_host,
    alt_hosts="clickhouse-node2, clickhouse-node3, clickhouse-node4",
)


def create_clickhouse_db():
    clickhouse_client.execute(
        "CREATE DATABASE IF NOT EXISTS movies_events ON CLUSTER company_cluster"
    )
    clickhouse_client.execute(
        """
        CREATE TABLE IF NOT EXISTS movies_events.regular_table ON CLUSTER company_cluster
            (
                user_id String,
                movie_id String,
                timestamp_of_film String
            )
            Engine=MergeTree()
        ORDER BY user_id
        """
    )


@backoff.on_exception(**backoff_settings)
def bulk_load_to_clickhouse(events):
    clickhouse_client.execute(
        """
        INSERT INTO movies_events.regular_table
            (
                user_id,
                movie_id,
                timestamp_of_film
            )
        VALUES
        """,
        (
            (
                event.user_id,
                event.movie_id,
                event.timestamp_of_film
            )
            for event in events
        ),
    )


def load_to_clickhouse(event):
    clickhouse_client.execute(
        """
        INSERT INTO movies_events.regular_table
            (
                user_id,
                movie_id,
                data
            )
        VALUES
        """,
        (
            event.user_id,
            event.movie_id,
            event.timestamp_of_film
        ),
    )
