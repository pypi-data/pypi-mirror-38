class APIRequestError(ValueError):
    pass

class APIObjectDeniedError(APIRequestError):
    pass

class APIRequestErrorOfflineDaemon(APIRequestError):
    pass

class APIRequestErrorOfflineDatastore(APIRequestError):
    pass

class IOHoldException(Exception):
    pass

class APIRemoteError(Exception):
    pass

class APIInvalidRequest(Exception):
    pass
