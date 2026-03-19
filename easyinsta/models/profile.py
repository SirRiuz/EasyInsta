"""
Profile data model.

This module contains the complete data model for profile information.
"""

from easyinsta.models.base import BaseModel


class Profile(BaseModel):
    """
    Complete profile data model.

    Represents detailed profile information returned by the Instagram API.

    Attributes:
        id (str): The unique profile ID (pk).
        fbid (str): The Facebook ID associated with the account.
        username (str): The profile username.
        full_name (str): The user's display name.
        biography (str): The profile bio text.
        profile_pic_url (str): URL to the standard profile picture (150x150).
        profile_pic_url_hd (str): URL to the HD profile picture (1080x1080).
        is_private (bool): Whether the account is set to private.
        is_verified (bool): Whether the account has the blue verification badge.
        is_business (bool): Whether the account is a business/creator account.
        is_memorialized (bool): Whether the account is memorialized.
        follower_count (int): Number of followers.
        following_count (int): Number of accounts being followed.
        media_count (int): Number of posts.
        total_clips_count (int): Number of Reels.
        external_url (str): External website URL in the profile.
        category (str | None): Business category (if applicable).
        has_highlight_reels (bool): Whether the account has story highlights.
        has_guides (bool): Whether the account has guides.
        is_active_on_text_post_app (bool): Whether the account is active on Threads.
        is_whatsapp_linked (bool): Whether WhatsApp is linked to the account.
        allow_mention_setting (str): Who can mention the user ("everyone", "following", "no_one").
        allow_tag_setting (str): Who can tag the user ("everyone", "following", "no_one").
        last_seen_timezone (str): The user's timezone.
        raw (dict): The complete raw API response data.
    """

    def __init__(self, data: dict):
        """
        Initialize a Profile instance.

        Args:
            data: The raw API response data (user object).
        """
        super().__init__(data)

        # Basic info
        self.id: str = data.get("pk", "")
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
        self.is_memorialized: bool = data.get("is_memorialized", False)

        # Counts
        self.follower_count: int = data.get("follower_count", 0)
        self.following_count: int = data.get("following_count", 0)
        self.media_count: int = data.get("media_count", 0)
        self.total_clips_count: int = data.get("total_clips_count", 0)

        # Additional info
        self.external_url: str = data.get("external_url", "")
        self.category: str | None = data.get("category")
        self.has_highlight_reels: bool = data.get("has_highlight_reels", False)
        self.has_guides: bool = data.get("has_guides", False)
        self.is_active_on_text_post_app: bool = data.get("is_active_on_text_post_app", False)
        self.is_whatsapp_linked: bool = data.get("is_whatsapp_linked", False)

        # Privacy settings
        self.allow_mention_setting: str = data.get("allow_mention_setting", "everyone")
        self.allow_tag_setting: str = data.get("allow_tag_setting", "everyone")

        # Location
        self.last_seen_timezone: str = data.get("last_seen_timezone", "")

    def __repr__(self) -> str:
        return f"Profile(id='{self.id}', username='{self.username}', full_name='{self.full_name}')"
