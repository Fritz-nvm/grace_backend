class APIException(RuntimeError):
    """Base class for all application-specific exceptions."""

    def __init__(self, message: str = "An application error occurred", *args):
        self.message = message
        self.args = args or (message,)  # Store arguments explicitly
        super().__init__(self.message, *self.args)

    def __str__(self):
        """Returns the primary error message."""
        return self.message

    def __repr__(self):
        """Returns a canonical representation of the exception."""
        return f"{self.__class__.__name__}(message='{self.message}', args={self.args})"


class PackageNotFoundError(APIException):
    """Raised when a requested Package ID does not exist in the database."""

    def __init__(self, message: str = "Package not found.", *args):
        super().__init__(message, *args)


class PackageAlreadyExistsError(APIException):
    """Raised when trying to create a Package with a name that already exists."""

    def __init__(
        self, message: str = "A package with this name already exists.", *args
    ):
        super().__init__(message, *args)
