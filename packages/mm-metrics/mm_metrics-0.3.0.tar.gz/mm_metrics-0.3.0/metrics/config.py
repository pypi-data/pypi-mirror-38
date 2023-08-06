from metrics.logger import logger
import os

try:
    from dotenv import find_dotenv, load_dotenv
    load_dotenv(find_dotenv())
except ImportError:
    logger.info('no dotenv library')


DD_API_KEY = os.environ.get('DD_API_KEY')
DD_APP_KEY = os.environ.get('DD_APP_KEY')
DD_STATSD_SOCKET_PATH = os.environ.get('DD_STATSD_SOCKET_PATH', '/var/run/datadog/dsd.socket')
DEFAULT_BACKEND = os.environ.get('METRICS_DEFAULT_BACKEND', 'metrics.backends.DataDogMetricsBackend')
