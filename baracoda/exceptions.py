class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class InvalidPrefixError(Error):
    """Raised when a prefix for a Heron barcode does not pass regex validation."""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        default_message = "Invalid prefix for Heron barcode"

        if self.message:
            return f"InvalidPrefixError: {self.message}"
        else:
            return f"InvalidPrefixError: {default_message}"
