import aiohttp

from easyinsta.exceptions import ApiError
from easyinsta.utils.agents import get_random_user_agent


BASE_URL = "https://i.instagram.com"


DEFAULT_HEADERS: dict[str, str] = {
    "X-Ig-App-Id": "936619743392459",
    "X-Ig-Capabilities": "3brTvwE=",
    "X-Ig-Connection-Type": "WIFI",
    "Accept-Language": "en-US",
    "Content-Type": "application/x-www-form-urlencoded",
}


async def api_call(
    path: str,
    method: str = "POST",
    body: dict | None = None,
    headers: dict | None = None,
) -> dict:
    """
    Make an async request to the Instagram API.

    Args:
        path: The API endpoint path.
        method: The HTTP method (GET, POST, etc.).
        body: The request body data (for POST requests).
        headers: Optional additional headers to include.

    Returns:
        The JSON response as a dictionary.

    Raises:
        ApiError: If the API returns a status code other than 200.
    """
    request_headers = {
        "User-Agent": get_random_user_agent(),
        **DEFAULT_HEADERS,
        **(headers or {}),
    }

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method,
            f"{BASE_URL}{path}",
            headers=request_headers,
            data=body,
        ) as response:
            if response.status != 200:
                raise ApiError(response.status)

            return await response.json()
