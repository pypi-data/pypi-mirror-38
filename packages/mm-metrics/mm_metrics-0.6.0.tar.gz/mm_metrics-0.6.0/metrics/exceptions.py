class BackendConnectionException(Exception):
    """ thrown when connection to a stats backend fails. This can either be due to connectivity issues, or due to a
     misconfiguration (like missing keys)
    """
    pass


class InvalidBackendException(Exception):
    """ thrown when trying to instantiate an invalid MetricsBackend (for instance, if it isn't a subclass of MetricsBackend """
    pass