"""
Profile light data model.

This module contains the data model for lightweight profile information.
"""

from easyinsta.models.base import BaseModel


class ProfileLight(BaseModel):
    """
    Lightweight profile data model.

    Represents basic profile information returned by the Instagram API.

    Attributes:
        id (str): The profile ID.
        username (str): The profile username.
        profile_pic_url (str): URL to the profile picture.
        raw (dict): The complete raw API response data.
    """

    def __init__(self, data: dict):
        """
        Initialize a ProfileLight instance.

        Args:
            data: The raw API response data.
        """
        super().__init__(data)
        self.id: str = data.get("pk", "")
        self.username: str = data.get("username", "")
        self.profile_pic_url: str = data.get("profile_pic_url", "")

    def __repr__(self) -> str:
        return f"ProfileLight(id='{self.id}', username='{self.username}')"
