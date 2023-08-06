class MetricsBackend(object):
    def connect(self, **connection_kwargs):
        return

    def increment(self, metric, **extra):
        raise NotImplemented

    def gauge(self, metric, value, **extra):
        raise NotImplemented

    def timed(self, metric, duration, **extra):
        raise NotImplemented
