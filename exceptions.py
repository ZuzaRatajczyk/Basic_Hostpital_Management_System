
class InvalidInputValue(Exception):
    """Raised when the input value is not correct"""
    pass


class InvalidPersonalId(Exception):
    """Raised when personal_id is not correct"""
    pass


class DbNotExist(Exception):
    """Raised when personal_id is not correct"""
    pass


class WrongCredentials(Exception):
    """Raised when database credentials are not correct"""
    pass
