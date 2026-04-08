"""
Base module class.

This module contains the abstract base class for all modules that require authentication.
"""

from abc import ABC
from functools import wraps
from typing import TYPE_CHECKING

from easyinsta.exceptions import AuthRequiredError

if TYPE_CHECKING:
    from easyinsta.modules.auth import Auth


def requires_auth(func):
    """
    Decorator that ensures the user is authenticated before executing the method.

    Raises:
        AuthRequiredError: If no authentication is configured.
    """
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if not self._auth.is_authenticated:
            raise AuthRequiredError()
        return await func(self, *args, **kwargs)
    return wrapper


class AuthenticatedModule(ABC):
    """
    Abstract base class for modules that require authentication.

    Provides access to the Auth instance for authenticated API requests.
    """

    def __init__(self, auth: "Auth"):
        self._auth = auth

    def _get_credentials(self) -> dict:
        """
        Get authentication headers for API requests.

        Returns:
            A dictionary with auth headers if authenticated, empty dict otherwise.
        """
        return self._auth.headers
