class ProfileNotFoundError(Exception):
    """
    Raised when a profile is not found.

    Attributes:
        profile_id: The ID of the profile that was not found.
    """

    def __init__(self, profile_id: str):
        self.profile_id = profile_id
        super().__init__("Profile not found")
