"""Tests for Validators module."""

from unittest.mock import AsyncMock, patch

import pytest

from easyinsta.exceptions import InvalidFormatError, MissingFieldError
from easyinsta.modules.validators import Validators


class TestValidatorsCheckUsername:
    """Tests for Validators.check_username method."""

    @pytest.mark.asyncio
    async def test_returns_true_when_username_exists(self):
        """Should return True when username is taken (not available)."""
        with patch("easyinsta.modules.validators.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"available": False}
            validators = Validators()
            result = await validators.check_username("existinguser")

        assert result is True

    @pytest.mark.asyncio
    async def test_returns_false_when_username_available(self):
        """Should return False when username is available."""
        with patch("easyinsta.modules.validators.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"available": True}
            validators = Validators()
            result = await validators.check_username("newuser")

        assert result is False

    @pytest.mark.asyncio
    async def test_raises_missing_field_error(self):
        """Should raise MissingFieldError when response lacks 'available' field."""
        with patch("easyinsta.modules.validators.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {}
            validators = Validators()

            with pytest.raises(MissingFieldError) as exc_info:
                await validators.check_username("testuser")

        assert exc_info.value.field == "available"


class TestValidatorsCheckEmail:
    """Tests for Validators.check_email method."""

    @pytest.mark.asyncio
    async def test_returns_true_when_email_taken(self):
        """Should return True when email is taken (not available)."""
        with patch("easyinsta.modules.validators.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"valid": True, "available": False}
            validators = Validators()
            result = await validators.check_email("taken@example.com")

        assert result is True

    @pytest.mark.asyncio
    async def test_returns_false_when_email_available(self):
        """Should return False when email is available."""
        with patch("easyinsta.modules.validators.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"valid": True, "available": True}
            validators = Validators()
            result = await validators.check_email("available@example.com")

        assert result is False

    @pytest.mark.asyncio
    async def test_raises_missing_field_error_for_valid(self):
        """Should raise MissingFieldError when response lacks 'valid' field."""
        with patch("easyinsta.modules.validators.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {}
            validators = Validators()

            with pytest.raises(MissingFieldError) as exc_info:
                await validators.check_email("test@example.com")

        assert exc_info.value.field == "valid"

    @pytest.mark.asyncio
    async def test_raises_invalid_format_error(self):
        """Should raise InvalidFormatError when email format is invalid."""
        with patch("easyinsta.modules.validators.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"valid": False}
            validators = Validators()

            with pytest.raises(InvalidFormatError) as exc_info:
                await validators.check_email("invalid-email")

        assert exc_info.value.field == "email"

    @pytest.mark.asyncio
    async def test_raises_missing_field_error_for_available(self):
        """Should raise MissingFieldError when response lacks 'available' field."""
        with patch("easyinsta.modules.validators.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"valid": True}
            validators = Validators()

            with pytest.raises(MissingFieldError) as exc_info:
                await validators.check_email("test@example.com")

        assert exc_info.value.field == "available"
