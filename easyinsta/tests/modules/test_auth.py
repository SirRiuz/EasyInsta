"""Tests for Auth module."""

import pytest

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
