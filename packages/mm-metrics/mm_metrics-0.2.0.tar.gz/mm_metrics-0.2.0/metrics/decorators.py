from functools import wraps


def increment(backend, on_start_metric=None, on_complete_metric=None, on_error_metric=None):
    def _inner(fn):
        @wraps(fn)
        def _decorator(*args, **kwargs):
            if on_start_metric:
                backend.increment(on_start_metric)

            try:
                result = fn(*args, **kwargs)
            except Exception as exc:
                if on_error_metric:
                    backend.increment(on_error_metric)

                raise exc

            if on_complete_metric:
                backend.increment(on_complete_metric)

            return result

        return _decorator

    return _inner