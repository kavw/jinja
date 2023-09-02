
class ValidationError(ValueError):
    pass


class TooFewArguments(ValidationError):
    pass


class TooMuchArguments(ValidationError):
    pass


class InvalidJson(ValidationError):
    pass


class InvalidPath(ValidationError):
    pass


class InvalidDir(ValidationError):
    pass
