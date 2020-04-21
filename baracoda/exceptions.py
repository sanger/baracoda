class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class WrongPrefixError(Error):
    """Raised when the prefix does not comply with the required format.
    """

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return f"WrongPrefixError: Prefix should be an alphanumeric uppercased string of up to 10 characters size"
