class ConfigurationError(Exception):
    pass


class BundleConfigurationError(ConfigurationError):
    def __init__(self, key, message):
        self.key = key

        super().__init__(message)


class OperationConfigurationError(ConfigurationError):
    def __init__(self, index, message):
        self.index = index

        super().__init__(message)


class OperationError(Exception):
    pass


class OperationFailedError(OperationError):
    pass


class OperationResponseError(OperationError):
    pass


class NoMoreRetriesError(OperationError):
    pass


class BundleError(Exception):
    pass


class BundleValidationError(BundleError):
    pass
