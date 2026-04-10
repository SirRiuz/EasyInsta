"""
Authentication module for Instagram API.

This module handles authentication state and provides auth headers for API requests.
"""

import base64
import json
import time
import uuid
from http import HTTPStatus

from easyinsta.constants import AuthPrefix, Endpoints, ErrorTypes, Headers
from easyinsta.exceptions import (
    AuthenticationError,
    InvalidPasswordError,
    InvalidUserError,
)
from easyinsta.utils.http import api_call


class Auth:
    """
    Authentication handler for Instagram API.

    Manages authentication tokens and provides headers for authenticated requests.
    """

    def __init__(self):
        self._token: str | None = None

    @property
    def is_authenticated(self) -> bool:
        """Check if the user is authenticated."""
        return self._token is not None

    @property
    def headers(self) -> dict:
        """
        Get authentication headers for API requests.

        Returns:
            A dictionary with the Authorization header if authenticated,
            empty dictionary otherwise.
        """
        if self._token is None:
            return {}

        return {"Authorization": f"Bearer IGT:2:{self._token}"}

    def with_token(self, token: str) -> None:
        """
        Authenticate manually using a pre-existing token.

        Use this method when you already have a valid Instagram token
        (for example, saved from a previous session or obtained externally).

        Note:
            This method does not validate the token. It simply stores it
            for use in subsequent API requests.

        Args:
            token: The Instagram token (base64 encoded JSON with ds_user_id
                and sessionid).

        Example:
            >>> ig = Instagram()
            >>> ig.auth.with_token("eyJkc191c2VyX2lkIjo...")
            >>> ig.auth.is_authenticated
            True
        """
        self._token = token

    def logout(self) -> None:
        """Clear the current authentication."""
        self._token = None

    def with_cookies(self, sessionid: str, ds_user_id: str) -> None:
        """
        Authenticate using Instagram cookies.

        Generates a token from sessionid and ds_user_id cookies. You can obtain
        these cookies from your browser's developer tools:

        1. Log in to Instagram in your browser (instagram.com)
        2. Open Developer Tools (F12 or Ctrl+Shift+I)
        3. Go to Application tab > Cookies > instagram.com
        4. Find and copy the values of "sessionid" and "ds_user_id" cookies

        Note:
            This method does not require an async call.

        Args:
            sessionid: The "sessionid" cookie value from instagram.com.
            ds_user_id: The "ds_user_id" cookie value from instagram.com.

        Example:
            >>> ig = Instagram()
            >>> ig.auth.with_cookies(
            ...     sessionid="14957970267%3AVBCu4jqK1b7aW4%3A20%3AAYh...",
            ...     ds_user_id="14957970267"
            ... )
            >>> ig.auth.is_authenticated
            True
        """
        payload = {"ds_user_id": ds_user_id, "sessionid": sessionid}
        token = base64.b64encode(json.dumps(payload).encode()).decode()
        self._token = token

    async def login(self, username: str, password: str) -> None:
        """
        Authenticate using Instagram username and password.

        Makes a login request to the Instagram API and stores the token
        from the response.

        Note:
            This method requires an async call.

        Args:
            username: The Instagram username.
            password: The Instagram password.

        Raises:
            InvalidUserError: If the username does not exist.
            InvalidPasswordError: If the password is incorrect.
            AuthenticationError: If the login fails for other reasons.

        Example:
            >>> ig = Instagram()
            >>> await ig.auth.login("your_username", "your_password")
            >>> ig.auth.is_authenticated
            True
        """
        device_id = f"android-{uuid.uuid4().hex[:16]}"
        guid = str(uuid.uuid4())
        timestamp = int(time.time())

        body = {
            "username": username,
            "enc_password": f"#PWD_INSTAGRAM:0:{timestamp}:{password}",
            "device_id": device_id,
            "guid": guid,
        }

        data = await api_call(
            Endpoints.LOGIN,
            method="POST",
            body=body,
            raise_exception=False,
        )

        context = data.get("response_context", {})
        status_code = context.get("status_code")
        headers = context.get("headers", {})

        # Handle error responses based on HTTP status code
        if status_code != HTTPStatus.OK:
            error_type = data.get("error_type")

            # Check for specific error types on 400 Bad Request
            if status_code == HTTPStatus.BAD_REQUEST and error_type:
                if error_type == ErrorTypes.BAD_PASSWORD:
                    raise InvalidPasswordError()
                if error_type == ErrorTypes.INVALID_USER:
                    raise InvalidUserError()

            # Generic authentication error for other failures
            raise AuthenticationError()

        # Extract token from response header
        auth_header = headers.get(Headers.SET_AUTHORIZATION, "")
        token = auth_header.replace(AuthPrefix.BEARER_IGT2, "")
        self._token = token
