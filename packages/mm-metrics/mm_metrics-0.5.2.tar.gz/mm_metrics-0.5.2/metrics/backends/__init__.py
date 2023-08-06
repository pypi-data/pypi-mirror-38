from .base import MetricsBackend
from .dd import DataDogMetricsBackend
from metrics.exceptions import InvalidBackendException
from metrics import config
import inspect


def backend_factory(backend_kls):
    if backend_kls is None:
        raise ValueError('the passed backend must be a Class')

    if not issubclass(backend_kls, MetricsBackend):
        raise InvalidBackendException('backend {} is not a valid MetricsBackend as it doesnt extend MetricsBackend'.format(backend_kls))

    # we introspect on the backend constructors' kwargs to know which config vars to use as params
    try:
        spec = inspect.getfullargspec(backend_kls.__init__)
    except AttributeError:
        # if we're in a 2.x env
        spec = inspect.getargspec(backend_kls.__init__)

    spec_args = spec.args

    backend_kwargs = {}
    backend_prefix_map = {
        'DataDogMetricsBackend': 'DD'
    }

    for arg in spec_args:
        if arg == 'self':
            continue

        backend_kwargs[arg] = getattr(config, '{}_{}'.format(backend_prefix_map[backend_kls.__name__], arg.upper()))

    return backend_kls(**backend_kwargs)
