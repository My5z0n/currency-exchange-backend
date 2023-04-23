class UserInputError(Exception):
    pass


class InternalServiceError(Exception):
    pass


class ConfigError(InternalServiceError):
    pass


class RepositoryError(InternalServiceError):
    pass
