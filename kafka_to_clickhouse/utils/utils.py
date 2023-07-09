import logging
from functools import wraps
from time import sleep

logger = logging.getLogger(__name__)


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции
    через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора
    до граничного времени ожидания.
    """

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            sleep_iter = 0
            while True:
                try:
                    res = func(*args, **kwargs)
                    return res
                except Exception as error:
                    logger.info("Exception: \n%s", error)
                    logger.info("Start sleeping for %s seconds (%s iter)", sleep_time, sleep_iter)
                    sleep(sleep_time)

                    sleep_iter += 1
                    sleep_time *= factor

                    if sleep_time >= border_sleep_time:
                        sleep_time = border_sleep_time

        return inner

    return wrapper
