class RateLimitError(Exception):
    """
    Raised when the API rate limit is exceeded.
    """

    def __init__(self):
        super().__init__("Too many requests. Please wait before trying again.")
