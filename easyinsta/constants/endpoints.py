"""
Instagram API endpoints.

This module centralizes all API endpoint paths used by the library.
"""


class Endpoints:
    """Instagram API endpoint paths."""

    # Users
    CHECK_USERNAME = "/api/v1/users/check_username/"
    CHECK_EMAIL = "/api/v1/users/check_email/"

    # Profiles
    PROFILE_LIGHT = "/api/v1/users/{profile_id}/info/"
    PROFILE_BY_USERNAME = "/api/v1/users/{username}/usernameinfo/"

    # Direct Messages
    INBOX = "/api/v1/direct_v2/inbox/"

    # Friendships
    FRIENDSHIP_CREATE = "/api/v1/friendships/create/{user_id}/"
    FRIENDSHIP_DESTROY = "/api/v1/friendships/destroy/{user_id}/"
