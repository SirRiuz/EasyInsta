class AuthenticationError(Exception):
    """
    Raised when login fails due to invalid username or password.
    """

    def __init__(self, message: str = "Invalid username or password"):
        self.message = message
        super().__init__(self.message)


class InvalidPasswordError(AuthenticationError):
    """
    Raised when login fails due to incorrect password.
    """

    def __init__(self, message: str = "Invalid password"):
        super().__init__(message)


class InvalidUserError(AuthenticationError):
    """
    Raised when login fails because the user does not exist.
    """

    def __init__(self, message: str = "User not found"):
        super().__init__(message)
