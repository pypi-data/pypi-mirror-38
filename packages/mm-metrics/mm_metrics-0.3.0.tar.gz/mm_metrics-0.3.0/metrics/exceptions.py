class BackendConnectionException(Exception):
    """ thrown when connection to a stats backend fails. This can either be due to connectivity issues, or due to a
     misconfiguration (like missing keys)
    """
    pass