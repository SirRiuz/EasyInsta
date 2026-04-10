"""Tests for Auth module."""

import base64
import json
from unittest.mock import AsyncMock, patch

import pytest

from easyinsta.exceptions import AuthenticationError, InvalidPasswordError, InvalidUserError
from easyinsta.modules.auth import Auth


class TestAuth:
    """Tests for Auth class."""

    def test_not_authenticated_by_default(self):
        """Should not be authenticated by default."""
        auth = Auth()
        assert auth.is_authenticated is False

    def test_headers_empty_when_not_authenticated(self):
        """Should return empty headers when not authenticated."""
        auth = Auth()
        assert auth.headers == {}

    def test_with_token_sets_authenticated(self):
        """Should be authenticated after setting token."""
        auth = Auth()
        auth.with_token("test_token")
        assert auth.is_authenticated is True

    def test_headers_contain_authorization_when_authenticated(self):
        """Should return Authorization header when authenticated."""
        auth = Auth()
        auth.with_token("test_token")
        assert "Authorization" in auth.headers
        assert auth.headers["Authorization"] == "Bearer IGT:2:test_token"

    def test_logout_clears_authentication(self):
        """Should clear authentication on logout."""
        auth = Auth()
        auth.with_token("test_token")
        auth.logout()
        assert auth.is_authenticated is False
        assert auth.headers == {}

    def test_token_format(self):
        """Should format token correctly with IGT:2 prefix."""
        auth = Auth()
        auth.with_token("eyJkc191c2VyX2lkIjoiMTIzNDU2Nzg5In0=")
        assert auth.headers["Authorization"] == "Bearer IGT:2:eyJkc191c2VyX2lkIjoiMTIzNDU2Nzg5In0="


class TestWithCookies:
    """Tests for Auth.with_cookies method."""

    def test_sets_authenticated(self):
        """Should be authenticated after setting cookies."""
        auth = Auth()
        auth.with_cookies(sessionid="session123", ds_user_id="123456")
        assert auth.is_authenticated is True

    def test_generates_valid_token(self):
        """Should generate a valid base64 encoded token."""
        auth = Auth()
        auth.with_cookies(sessionid="session123", ds_user_id="123456")

        # Extract token from header
        header = auth.headers["Authorization"]
        token = header.replace("Bearer IGT:2:", "")

        # Decode and verify
        decoded = json.loads(base64.b64decode(token).decode())
        assert decoded["ds_user_id"] == "123456"
        assert decoded["sessionid"] == "session123"

    def test_headers_contain_authorization(self):
        """Should return Authorization header when authenticated with cookies."""
        auth = Auth()
        auth.with_cookies(sessionid="session123", ds_user_id="123456")
        assert "Authorization" in auth.headers
        assert auth.headers["Authorization"].startswith("Bearer IGT:2:")

    def test_with_real_cookie_format(self):
        """Should work with real Instagram cookie format."""
        auth = Auth()
        auth.with_cookies(
            sessionid="14957970267%3AVBCu4jqK1b7aW4%3A20%3AAYhClGTgFO3b0jIID2XkQ3xPjVwM7Op7xYuiq6d71g",
            ds_user_id="14957970267"
        )

        header = auth.headers["Authorization"]
        token = header.replace("Bearer IGT:2:", "")
        decoded = json.loads(base64.b64decode(token).decode())

        assert decoded["ds_user_id"] == "14957970267"
        assert "14957970267" in decoded["sessionid"]


class TestLogin:
    """Tests for Auth.login method."""

    @pytest.mark.asyncio
    async def test_sets_authenticated_on_success(self):
        """Should be authenticated after successful login."""
        mock_return = {
            "status": "ok",
            "response_context": {
                "status_code": 200,
                "headers": {"ig-set-authorization": "Bearer IGT:2:test_token"},
            },
        }

        with patch("easyinsta.modules.auth.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = mock_return
            auth = Auth()
            await auth.login("testuser", "testpass")

        assert auth.is_authenticated is True

    @pytest.mark.asyncio
    async def test_extracts_token_from_response_header(self):
        """Should extract token from Ig-Set-Authorization header."""
        mock_return = {
            "status": "ok",
            "response_context": {
                "status_code": 200,
                "headers": {"ig-set-authorization": "Bearer IGT:2:extracted_token"},
            },
        }

        with patch("easyinsta.modules.auth.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = mock_return
            auth = Auth()
            await auth.login("testuser", "testpass")

        assert auth.headers["Authorization"] == "Bearer IGT:2:extracted_token"

    @pytest.mark.asyncio
    async def test_raises_invalid_password_error(self):
        """Should raise InvalidPasswordError when password is wrong."""
        mock_return = {
            "status": "fail",
            "error_type": "bad_password",
            "response_context": {
                "status_code": 400,
                "headers": {},
            },
        }

        with patch("easyinsta.modules.auth.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = mock_return
            auth = Auth()

            with pytest.raises(InvalidPasswordError):
                await auth.login("testuser", "wrongpass")

    @pytest.mark.asyncio
    async def test_raises_invalid_user_error(self):
        """Should raise InvalidUserError when user does not exist."""
        mock_return = {
            "status": "fail",
            "error_type": "invalid_user",
            "response_context": {
                "status_code": 400,
                "headers": {},
            },
        }

        with patch("easyinsta.modules.auth.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = mock_return
            auth = Auth()

            with pytest.raises(InvalidUserError):
                await auth.login("nonexistent", "testpass")

    @pytest.mark.asyncio
    async def test_raises_authentication_error_on_generic_failure(self):
        """Should raise AuthenticationError on generic 400 error without error_type."""
        mock_return = {
            "status": "fail",
            "response_context": {
                "status_code": 400,
                "headers": {},
            },
        }

        with patch("easyinsta.modules.auth.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = mock_return
            auth = Auth()

            with pytest.raises(AuthenticationError):
                await auth.login("testuser", "testpass")

    @pytest.mark.asyncio
    async def test_raises_authentication_error_on_non_400_error(self):
        """Should raise AuthenticationError on non-400 status codes."""
        mock_return = {
            "status": "fail",
            "response_context": {
                "status_code": 500,
                "headers": {},
            },
        }

        with patch("easyinsta.modules.auth.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = mock_return
            auth = Auth()

            with pytest.raises(AuthenticationError):
                await auth.login("testuser", "testpass")
