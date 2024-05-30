class EmailAlreadyRegisteredError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class AuthNotPermissionError(Exception):
    pass


class InvalidJSONWebTokenError(Exception):
    pass
