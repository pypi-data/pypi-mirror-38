from functools import wraps
from metrics import metrics_backend
from metrics import context


def increment(backend=None, on_start_metric=None, on_complete_metric=None, on_error_metric=None, **extra):
    _backend = backend or metrics_backend

    def _inner(fn):
        @wraps(fn)
        def _decorator(*args, **kwargs):
            if on_start_metric:
                _backend.increment(on_start_metric, **extra)

            try:
                result = fn(*args, **kwargs)
            except Exception as exc:
                if on_error_metric:
                    _backend.increment(on_error_metric, **extra)

                raise exc

            if on_complete_metric:
                _backend.increment(on_complete_metric, **extra)

            return result

        return _decorator

    return _inner


def timer(backend=None, metric=None, **extra):
    _backend = backend or metrics_backend

    def _inner(fn):
        @wraps(fn)
        def _decorator(*args, **kwargs):
            with context.timer(backend=_backend, metric=metric, **extra):
                return fn(*args, **kwargs)

        return _decorator

    return _inner
