"""
Module utilities for direct messages.

This module contains helper functions for fetching inbox data from the API.
"""

from easyinsta.utils.http import api_call
from easyinsta.constants import Endpoints


async def fetch_inbox(
    headers: dict,
    cursor: str | None = None,
    limit: int = 20,
    filter_type: str = "unread",
) -> dict:
    """
    Fetch inbox data from the API.

    Args:
        headers: The authentication headers.
        cursor: The pagination cursor for fetching older threads.
        limit: The number of threads to fetch per request.
        filter_type: The filter type (e.g., "unread").

    Returns:
        The inbox data dictionary.
    """
    params = {
        "visual_message_return_type": "unseen",
        "selected_filter": filter_type,
        "limit": str(limit),
    }

    if cursor:
        params["cursor"] = cursor

    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    path = f"{Endpoints.INBOX}?{query_string}"

    return await api_call(path, method="GET", headers=headers)
