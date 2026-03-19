class MissingFieldError(Exception):
    """
    Raised when a required field is missing from an API response.

    Attributes:
        field: The name of the missing field.
    """

    def __init__(self, field: str):
        self.field = field
        super().__init__(f"Missing '{field}' field in response")
