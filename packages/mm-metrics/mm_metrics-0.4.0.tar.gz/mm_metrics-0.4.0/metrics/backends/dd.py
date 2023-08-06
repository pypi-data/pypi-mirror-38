from metrics.backends.base import MetricsBackend
from metrics import config, exceptions
from datadog import initialize, statsd
from functools import wraps
import time
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
    def __init__(self, service_name=None, service_priority=None, global_tags=None):
        """
        :param service_name: `str` the name of the service being monitored
        :param service_priority: `str` the service priority, on a scale of 1 to 5, 1 being the highest priority
        :param global_tags: `dict` of additional global tags to apply to all stats sent to DD
        """
        super(DataDogMetricsBackend, self).__init__()

        self.service_name = service_name
        self.service_priority = service_priority
        self.global_tags = global_tags or {}

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
        statsd.increment(metric, tags=self.statsd_tags)

        return True

    @requires_connection
    def gauge(self, metric, value):
        statsd.gauge(metric, value, tags=self.statsd_tags)

        return True

    @requires_connection
    def timed(self, metric, duration):
        statsd.histogram(metric, duration, tags=self.statsd_tags)

        return True

    @property
    def statsd_tags(self):
        """ the global statsd tags to apply to all statsd functions """
        tag_map = {
            'service': self.service_name,
            'priority': self.service_priority,
        }

        tag_map.update(self.global_tags)

        return [':'.join([tag, val]) for tag, val in tag_map.items() if val is not None]
