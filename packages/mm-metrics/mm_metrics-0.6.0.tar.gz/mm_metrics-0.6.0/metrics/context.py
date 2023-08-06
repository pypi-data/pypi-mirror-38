from contextlib import contextmanager
from metrics import metrics_backend
from metrics.logger import logger
import time


@contextmanager
def timer(backend=None, metric=None, **extra):
    """ timer context manager """
    _backend = backend or metrics_backend

    start_time = time.time()

    try:
        yield
    finally:
        end_time = time.time()

    delta = end_time - start_time

    logger.debug('{} -- {}'.format(metric, delta))

    _backend.timed(metric, delta, **extra)
