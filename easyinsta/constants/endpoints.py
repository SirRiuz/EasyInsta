"""
Instagram API endpoints.

This module centralizes all API endpoint paths used by the library.
"""


class Endpoints:
    """Instagram API endpoint paths."""

    # Auth
    LOGIN = "/api/v1/accounts/login/"
    CURRENT_USER = "/api/v1/accounts/current_user/"

    # Account settings
    SET_PUBLIC = "/api/v1/accounts/set_public/"
    SET_PRIVATE = "/api/v1/accounts/set_private/"
    CHANGE_PROFILE_PICTURE = "/api/v1/accounts/change_profile_picture/"
    REMOVE_PROFILE_PICTURE = "/api/v1/accounts/remove_profile_picture/"

    # Upload
    RUPLOAD_PHOTO = "/rupload_igphoto/{entity_name}/"

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
    FRIENDSHIP_SET_BESTIES = "/api/v1/friendships/set_besties/"
    FRIENDSHIP_BLOCK = "/api/v1/friendships/block/{user_id}/"
    FRIENDSHIP_UNBLOCK = "/api/v1/friendships/unblock/{user_id}/"
