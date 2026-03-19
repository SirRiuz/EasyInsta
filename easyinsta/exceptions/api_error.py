class ApiError(Exception):
    """
    Raised when the API returns a non-200 status code.

    Attributes:
        status_code: The HTTP status code returned by the API.
    """

    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"API error: {status_code}")
