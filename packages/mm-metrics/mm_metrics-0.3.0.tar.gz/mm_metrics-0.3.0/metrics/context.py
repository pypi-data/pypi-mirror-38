from contextlib import contextmanager
from metrics import metrics_backend
from metrics.utils import difference
from metrics.logger import logger
import datetime


@contextmanager
def timer(backend=None, metric=None, units='ms'):
    """ timer context manager """
    _backend = backend or metrics_backend

    start_dt = datetime.datetime.now()

    try:
        yield
    finally:
        end_dt = datetime.datetime.now()

    delta = difference(start_dt, end_dt, units=units)

    logger.debug('{} -- {}{}'.format(metric, delta, units))

    _backend.gauge(metric, delta)
