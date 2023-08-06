from pydoc import locate
from metrics.backends import backend_factory
from metrics import config

metrics_backend = backend_factory(locate(config.DEFAULT_BACKEND))
