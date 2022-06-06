class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class InvalidPrefixError(Error):
    """Raised when a prefix for a Heron barcode does not pass regex validation."""

    def __init__(self, message: str = ""):
        self.message = message

    def __str__(self):
        default_message = "Invalid prefix for Heron barcode"

        if self.message:
            return f"InvalidPrefixError: {self.message}"
        else:
            return f"InvalidPrefixError: {default_message}"


class InvalidCountError(Error):
    """Raised when a param count for a Heron barcode group or child barcode is not found."""

    def __init__(self, message: str = ""):
        self.message = message

    def __str__(self):
        default_message = "Please add the 'count' param to the request"

        if self.message:
            return f"InvalidCountError: {self.message}"
        else:
            return f"InvalidCountError: {default_message}"


class InvalidBarcodeError(Error):
    """Raised when a barcode param is not given for a child barcode"""

    def __init__(self, message: str = ""):
        self.message = message

    def __str__(self):
        default_message = "Please add the 'barcode' param to the request"

        if self.message:
            return f"InvalidBarcodeError: {self.message}"
        else:
            return f"InvalidBarcodeError: {default_message}"
