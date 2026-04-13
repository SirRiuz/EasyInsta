"""
Account data model.

This module contains the data model for the authenticated user's account.
"""

from easyinsta.models.base import BaseModel


class Account(BaseModel):
    """
    Account data model for the authenticated user.

    Represents the authenticated user's account information returned by
    the Instagram API's current_user endpoint.

    Attributes:
        id (str): The unique account ID (pk).
        fbid (str): The Facebook ID associated with the account.
        username (str): The account username.
        full_name (str): The user's display name.
        biography (str): The profile bio text.
        profile_pic_url (str): URL to the standard profile picture.
        profile_pic_url_hd (str): URL to the HD profile picture.
        is_private (bool): Whether the account is set to private.
        is_verified (bool): Whether the account has the blue verification badge.
        is_business (bool): Whether the account is a business/creator account.
        follower_count (int): Number of followers.
        following_count (int): Number of accounts being followed.
        media_count (int): Number of posts.
        phone_number (str): The phone number linked to the account.
        email (str): The email address linked to the account.
        birthday (str): The user's birthday.
        gender (int): The user's gender (1=male, 2=female, 3=custom).
        external_url (str): External website URL in the profile.
        raw (dict): The complete raw API response data.
    """

    def __init__(self, data: dict):
        """
        Initialize an Account instance.

        Args:
            data: The raw API response data (user object).
        """
        super().__init__(data)

        # Basic info
        self.id: str = str(data.get("pk", ""))
        self.fbid: str = data.get("fbid_v2", "")
        self.username: str = data.get("username", "")
        self.full_name: str = data.get("full_name", "")
        self.biography: str = data.get("biography", "")

        # Profile picture
        self.profile_pic_url: str = data.get("profile_pic_url", "")
        hd_pic_info = data.get("hd_profile_pic_url_info", {})
        self.profile_pic_url_hd: str = hd_pic_info.get("url", "")

        # Account status
        self.is_private: bool = data.get("is_private", False)
        self.is_verified: bool = data.get("is_verified", False)
        self.is_business: bool = data.get("is_business", False)

        # Counts
        self.follower_count: int = data.get("follower_count", 0)
        self.following_count: int = data.get("following_count", 0)
        self.media_count: int = data.get("media_count", 0)

        # Personal info (only available for own account)
        self.phone_number: str = data.get("phone_number", "")
        self.email: str = data.get("email", "")
        self.birthday: str = data.get("birthday", "")
        self.gender: int = data.get("gender", 0)

        # Additional info
        self.external_url: str = data.get("external_url", "")

    def __repr__(self) -> str:
        return f"Account(id='{self.id}', username='{self.username}')"
