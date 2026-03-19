"""
Module utilities for profile fetching.

This module contains helper functions for fetching profile data from the API.
"""

from http import HTTPStatus

from easyinsta.utils import api_call
from easyinsta.constants import Endpoints
from easyinsta.exceptions import ApiError, ProfileNotFoundError, RateLimitError


async def fetch_profile_by_username(username: str, headers: dict) -> dict:
    """
    Fetch profile data by username.

    Args:
        username: The Instagram username.
        headers: The authentication headers.

    Returns:
        The user data dictionary.

    Raises:
        ProfileNotFoundError: If the profile is not found.
        ApiError: If the API returns an error.
    """
    try:
        path = Endpoints.PROFILE_BY_USERNAME.format(username=username)
        data = await api_call(path, method="GET", headers=headers)
    except ApiError as e:
        if e.status_code == HTTPStatus.NOT_FOUND:
            raise ProfileNotFoundError(username)
        raise

    if "user" not in data:
        raise ProfileNotFoundError(username)

    return data["user"]


async def fetch_profile_by_id(profile_id: str, headers: dict) -> dict:
    """
    Fetch profile data by profile ID.

    Args:
        profile_id: The Instagram profile ID.
        headers: The authentication headers.

    Returns:
        The user data dictionary.

    Raises:
        ProfileNotFoundError: If the profile is not found.
        ApiError: If the API returns an error.
    """
    try:
        path = Endpoints.PROFILE_LIGHT.format(profile_id=profile_id)
        data = await api_call(path, method="GET", headers=headers)
    except ApiError as e:
        if e.status_code == HTTPStatus.NOT_FOUND:
            raise ProfileNotFoundError(profile_id)
        raise

    if "user" not in data:
        raise ProfileNotFoundError(profile_id)

    return data["user"]


async def fetch_profile_by_id_no_auth(profile_id: str) -> dict:
    """
    Fetch profile data by profile ID without authentication.

    Args:
        profile_id: The Instagram profile ID.

    Returns:
        The user data dictionary.

    Raises:
        ProfileNotFoundError: If the profile is not found.
        RateLimitError: If the API rate limit is exceeded.
        ApiError: If the API returns an error.
    """
    try:
        path = Endpoints.PROFILE_LIGHT.format(profile_id=profile_id)
        data = await api_call(path, method="GET")
    except ApiError as e:
        # Instagram API returns 401 (Unauthorized) instead of 429 (Too Many Requests)
        # when rate limiting unauthenticated requests. This is a known behavior
        # where excessive requests without authentication trigger a 401 response
        # as a form of rate limiting protection.
        if e.status_code == HTTPStatus.UNAUTHORIZED:
            raise RateLimitError()
        if e.status_code == HTTPStatus.NOT_FOUND:
            raise ProfileNotFoundError(profile_id)
        raise

    if "user" not in data:
        raise ProfileNotFoundError(profile_id)

    return data["user"]
