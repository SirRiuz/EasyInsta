"""Tests for module utilities."""

from unittest.mock import AsyncMock, patch

import pytest

from easyinsta.exceptions import ApiError, ProfileNotFoundError, RateLimitError
from easyinsta.modules.utils import (
    fetch_profile_by_id,
    fetch_profile_by_id_no_auth,
    fetch_profile_by_username,
)


class TestFetchProfileByUsername:
    """Tests for fetch_profile_by_username function."""

    @pytest.mark.asyncio
    async def test_returns_user_data(self):
        """Should return user data from response."""
        mock_user = {"pk": "123456", "username": "testuser"}

        with patch("easyinsta.modules.utils.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"user": mock_user}
            result = await fetch_profile_by_username("testuser", {"Authorization": "Bearer token"})

        assert result == mock_user

    @pytest.mark.asyncio
    async def test_raises_profile_not_found_on_404(self):
        """Should raise ProfileNotFoundError on 404 status."""
        with patch("easyinsta.modules.utils.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.side_effect = ApiError(404)

            with pytest.raises(ProfileNotFoundError) as exc_info:
                await fetch_profile_by_username("nonexistent", {})

        assert exc_info.value.profile_id == "nonexistent"

    @pytest.mark.asyncio
    async def test_raises_profile_not_found_when_no_user_in_response(self):
        """Should raise ProfileNotFoundError when 'user' not in response."""
        with patch("easyinsta.modules.utils.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {}

            with pytest.raises(ProfileNotFoundError):
                await fetch_profile_by_username("testuser", {})

    @pytest.mark.asyncio
    async def test_reraises_other_api_errors(self):
        """Should reraise non-404 ApiErrors."""
        with patch("easyinsta.modules.utils.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.side_effect = ApiError(500)

            with pytest.raises(ApiError) as exc_info:
                await fetch_profile_by_username("testuser", {})

        assert exc_info.value.status_code == 500


class TestFetchProfileById:
    """Tests for fetch_profile_by_id function."""

    @pytest.mark.asyncio
    async def test_returns_user_data(self):
        """Should return user data from response."""
        mock_user = {"pk": "123456", "username": "testuser"}

        with patch("easyinsta.modules.utils.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"user": mock_user}
            result = await fetch_profile_by_id("123456", {"Authorization": "Bearer token"})

        assert result == mock_user

    @pytest.mark.asyncio
    async def test_raises_profile_not_found_on_404(self):
        """Should raise ProfileNotFoundError on 404 status."""
        with patch("easyinsta.modules.utils.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.side_effect = ApiError(404)

            with pytest.raises(ProfileNotFoundError) as exc_info:
                await fetch_profile_by_id("123456", {})

        assert exc_info.value.profile_id == "123456"

    @pytest.mark.asyncio
    async def test_raises_profile_not_found_when_no_user_in_response(self):
        """Should raise ProfileNotFoundError when 'user' not in response."""
        with patch("easyinsta.modules.utils.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {}

            with pytest.raises(ProfileNotFoundError):
                await fetch_profile_by_id("123456", {})

    @pytest.mark.asyncio
    async def test_reraises_other_api_errors(self):
        """Should reraise non-404 ApiErrors."""
        with patch("easyinsta.modules.utils.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.side_effect = ApiError(500)

            with pytest.raises(ApiError) as exc_info:
                await fetch_profile_by_id("123456", {})

        assert exc_info.value.status_code == 500


class TestFetchProfileByIdNoAuth:
    """Tests for fetch_profile_by_id_no_auth function."""

    @pytest.mark.asyncio
    async def test_returns_user_data(self):
        """Should return user data from response."""
        mock_user = {"pk": "123456", "username": "testuser"}

        with patch("easyinsta.modules.utils.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"user": mock_user}
            result = await fetch_profile_by_id_no_auth("123456")

        assert result == mock_user

    @pytest.mark.asyncio
    async def test_raises_rate_limit_error_on_401(self):
        """Should raise RateLimitError on 401 status (rate limiting)."""
        with patch("easyinsta.modules.utils.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.side_effect = ApiError(401)

            with pytest.raises(RateLimitError):
                await fetch_profile_by_id_no_auth("123456")

    @pytest.mark.asyncio
    async def test_raises_profile_not_found_on_404(self):
        """Should raise ProfileNotFoundError on 404 status."""
        with patch("easyinsta.modules.utils.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.side_effect = ApiError(404)

            with pytest.raises(ProfileNotFoundError) as exc_info:
                await fetch_profile_by_id_no_auth("123456")

        assert exc_info.value.profile_id == "123456"

    @pytest.mark.asyncio
    async def test_raises_profile_not_found_when_no_user_in_response(self):
        """Should raise ProfileNotFoundError when 'user' not in response."""
        with patch("easyinsta.modules.utils.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {}

            with pytest.raises(ProfileNotFoundError):
                await fetch_profile_by_id_no_auth("123456")

    @pytest.mark.asyncio
    async def test_reraises_other_api_errors(self):
        """Should reraise non-401/404 ApiErrors."""
        with patch("easyinsta.modules.utils.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.side_effect = ApiError(500)

            with pytest.raises(ApiError) as exc_info:
                await fetch_profile_by_id_no_auth("123456")

        assert exc_info.value.status_code == 500
