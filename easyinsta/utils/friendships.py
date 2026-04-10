"""
Module utilities for friendships.

This module contains helper functions for follow/unfollow and close friends actions.
"""

import json

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


async def add_close_friend(user_id: str, headers: dict) -> dict:
    """
    Add a user to close friends list.

    Args:
        user_id: The Instagram user ID to add.
        headers: The authentication headers.

    Returns:
        The API response dictionary.
    """
    body = {"add": json.dumps([user_id]), "remove": json.dumps([])}
    return await api_call(
        Endpoints.FRIENDSHIP_SET_BESTIES,
        method="POST",
        body=body,
        headers=headers,
    )


async def remove_close_friend(user_id: str, headers: dict) -> dict:
    """
    Remove a user from close friends list.

    Args:
        user_id: The Instagram user ID to remove.
        headers: The authentication headers.

    Returns:
        The API response dictionary.
    """
    body = {"add": json.dumps([]), "remove": json.dumps([user_id])}
    return await api_call(
        Endpoints.FRIENDSHIP_SET_BESTIES,
        method="POST",
        body=body,
        headers=headers,
    )


async def block_user(user_id: str, headers: dict) -> dict:
    """
    Block a user.

    Args:
        user_id: The Instagram user ID to block.
        headers: The authentication headers.

    Returns:
        The API response dictionary.
    """
    path = Endpoints.FRIENDSHIP_BLOCK.format(user_id=user_id)
    body = {"user_id": user_id, "surface": "profile"}
    return await api_call(path, method="POST", body=body, headers=headers)


async def unblock_user(user_id: str, headers: dict) -> dict:
    """
    Unblock a user.

    Args:
        user_id: The Instagram user ID to unblock.
        headers: The authentication headers.

    Returns:
        The API response dictionary.
    """
    path = Endpoints.FRIENDSHIP_UNBLOCK.format(user_id=user_id)
    body = {"user_id": user_id, "container_module": "profile"}
    return await api_call(path, method="POST", body=body, headers=headers)
