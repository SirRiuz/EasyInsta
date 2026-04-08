"""
Authentication module for Instagram API.

This module handles authentication state and provides auth headers for API requests.
"""


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
        Authenticate using a JWT token.

        Args:
            token: The Instagram JWT token (base64 encoded).

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
