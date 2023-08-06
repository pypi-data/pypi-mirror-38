from pydoc import locate
from metrics import config

metrics_backend = locate(config.DEFAULT_BACKEND)()
