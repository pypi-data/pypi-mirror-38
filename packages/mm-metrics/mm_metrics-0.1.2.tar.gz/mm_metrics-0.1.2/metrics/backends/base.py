class MetricsBackend(object):
    def connect(self, **connection_kwargs):
        return

    def increment(self, metric):
        raise NotImplemented

    def gauge(self, metric, value):
        raise NotImplemented