
class UserInputError(Exception):
    def __init__(self, message):
        self.message = message


class ConfigError(Exception):
    def __init__(self, message):
        self.message = message
