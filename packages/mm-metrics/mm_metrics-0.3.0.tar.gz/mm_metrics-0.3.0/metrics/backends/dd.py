from metrics.backends.base import MetricsBackend
from metrics import config, exceptions
from datadog import initialize, statsd
from functools import wraps

import os


def requires_connection(fn):
    @wraps(fn)
    def _inner(self, *args, **kwargs):
        if not self._connected:
            self.connect()

            # if we are still not connected, it means the connection credentials weren't loaded in the env
            if not self._connected:
                raise exceptions.BackendConnectionException('you must call dd.connect() with connection_kwargs')

        result = fn(self, *args, **kwargs)

        return result

    return _inner


class DataDogMetricsBackend(MetricsBackend):
    def __init__(self):
        super(DataDogMetricsBackend, self).__init__()

        self._connected = False

    def connect(self, **connection_kwargs):
        options = {
            'api_key': connection_kwargs.pop('api_key', config.DD_API_KEY),
            'app_key': connection_kwargs.pop('app_key', config.DD_APP_KEY),
            'statsd_socket_path': connection_kwargs.pop('statsd_socket_path', config.DD_STATSD_SOCKET_PATH),
        }

        if not options['api_key'] or not options['app_key']:
            raise exceptions.BackendConnectionException('the DataDog backend requires keys to either be set in the env, or passed to the `connect` method')

        initialize(**options)

        self._connected = True

    @requires_connection
    def increment(self, metric):
        statsd.increment(metric)

        return True

    @requires_connection
    def gauge(self, metric, value):
        statsd.gauge(metric, value)

        return True