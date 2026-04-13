from http import HTTPStatus

import aiohttp

from easyinsta.constants import AuthPrefix, RequestHeaders
from easyinsta.exceptions import ApiError


BASE_URL = "https://i.instagram.com"


def extract_token_from_headers(headers: dict | None) -> str | None:
    """
    Extract the Instagram authentication token from the Authorization header.

    Parses the Authorization header looking for the Bearer IGT:2: prefix
    used by Instagram's API and extracts the token portion.

    Args:
        headers: Dictionary of HTTP headers.

    Returns:
        The extracted token if Authorization header contains a valid
        Bearer IGT:2: token, None otherwise.
    """
    if not headers or RequestHeaders.AUTHORIZATION not in headers:
        return None

    auth_header = headers[RequestHeaders.AUTHORIZATION]

    if auth_header.startswith(AuthPrefix.BEARER_IGT2):
        return auth_header.replace(AuthPrefix.BEARER_IGT2, "")


async def api_call(
    path: str,
    method: str = "POST",
    body: dict | bytes | None = None,
    headers: dict | None = None,
    raise_exception: bool = True,
) -> dict:
    """
    Make an async request to the Instagram API.

    Args:
        path: The API endpoint path.
        method: The HTTP method (GET, POST, etc.).
        body: The request body data (dict for form-urlencoded, bytes for raw data).
        headers: Headers to include in the request.
        raise_exception: If False, won't raise ApiError on non-200 status.

    Returns:
        The JSON response as a dictionary.

    Raises:
        ApiError: If the API returns a status code other than 200 (unless raise_exception=False).
    """

    # # DEBUG: Burp-style request format
    # from urllib.parse import urlencode
    # print("\n" + "=" * 60)
    # print(f"{method} {path} HTTP/1.1")
    # print(f"Host: i.instagram.com")
    # if headers:
    #     for k, v in headers.items():
    #         print(f"{k}: {v}")
    # print()
    # if body:
    #     if isinstance(body, bytes):
    #         print(f"[BINARY DATA: {len(body)} bytes]")
    #     elif isinstance(body, dict):
    #         print(urlencode(body))
    #     else:
    #         print(body)
    # print("=" * 60 + "\n")

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method,
            f"{BASE_URL}{path}",
            headers=headers,
            data=body,
        ) as response:

            # Raise exception on non-200 status unless explicitly disabled
            if raise_exception and response.status != HTTPStatus.OK:
                raise ApiError(response.status)

            data = await response.json() or {}

            # Attach HTTP metadata (status code, headers) to the response
            # for cases like extracting auth tokens or handling errors
            data["response_context"] = {
                "status_code": response.status,
                "headers": dict(response.headers),
            }

            return data
