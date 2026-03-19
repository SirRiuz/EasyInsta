"""Tests for exception classes."""

import pytest

from easyinsta.exceptions import (
    ApiError,
    InvalidFormatError,
    MissingFieldError,
    ProfileNotFoundError,
    RateLimitError,
)


class TestApiError:
    """Tests for ApiError exception."""

    def test_stores_status_code(self):
        """Should store the status code."""
        error = ApiError(404)
        assert error.status_code == 404

    def test_message_contains_status_code(self):
        """Should include status code in message."""
        error = ApiError(500)
        assert "500" in str(error)


class TestInvalidFormatError:
    """Tests for InvalidFormatError exception."""

    def test_stores_field_name(self):
        """Should store the field name."""
        error = InvalidFormatError("email")
        assert error.field == "email"

    def test_message_contains_field_name(self):
        """Should include field name in message."""
        error = InvalidFormatError("email")
        assert "email" in str(error)


class TestMissingFieldError:
    """Tests for MissingFieldError exception."""

    def test_stores_field_name(self):
        """Should store the field name."""
        error = MissingFieldError("available")
        assert error.field == "available"

    def test_message_contains_field_name(self):
        """Should include field name in message."""
        error = MissingFieldError("available")
        assert "available" in str(error)


class TestProfileNotFoundError:
    """Tests for ProfileNotFoundError exception."""

    def test_stores_profile_id(self):
        """Should store the profile ID."""
        error = ProfileNotFoundError("123456")
        assert error.profile_id == "123456"

    def test_message(self):
        """Should have correct message."""
        error = ProfileNotFoundError("123456")
        assert "Profile not found" in str(error)


class TestRateLimitError:
    """Tests for RateLimitError exception."""

    def test_message(self):
        """Should have correct message."""
        error = RateLimitError()
        assert "Too many requests" in str(error)
