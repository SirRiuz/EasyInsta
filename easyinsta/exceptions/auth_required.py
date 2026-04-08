class AuthRequiredError(Exception):
    """
    Raised when an operation requires authentication but no auth is configured.
    """

    def __init__(self):
        super().__init__("Authentication required")
