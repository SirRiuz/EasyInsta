class InvalidFormatError(Exception):
    """
    Raised when a value has an invalid format.

    Attributes:
        field: The name of the field with invalid format.
    """

    def __init__(self, field: str):
        self.field = field
        super().__init__(f"Invalid '{field}' format")
