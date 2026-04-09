"""
Module utilities for friendships.

This module contains helper functions for follow/unfollow actions.
"""

from easyinsta.utils.http import api_call
from easyinsta.constants import Endpoints


async def follow_user(user_id: str, headers: dict) -> dict:
    """
    Follow a user.

    Args:
        user_id: The Instagram user ID to follow.
        headers: The authentication headers.

    Returns:
        The API response dictionary.
    """
    path = Endpoints.FRIENDSHIP_CREATE.format(user_id=user_id)
    body = {"user_id": user_id}
    return await api_call(path, method="POST", body=body, headers=headers)


async def unfollow_user(user_id: str, headers: dict) -> dict:
    """
    Unfollow a user.

    Args:
        user_id: The Instagram user ID to unfollow.
        headers: The authentication headers.

    Returns:
        The API response dictionary.
    """
    path = Endpoints.FRIENDSHIP_DESTROY.format(user_id=user_id)
    body = {"user_id": user_id}
    return await api_call(path, method="POST", body=body, headers=headers)
