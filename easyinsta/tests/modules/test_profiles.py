"""Tests for Profiles module."""

from unittest.mock import AsyncMock, patch

import pytest

from easyinsta.constants import ErrorMessages
from easyinsta.models import Profile, ProfileLight
from easyinsta.modules.profiles import Profiles


class TestProfilesGetPublic:
    """Tests for Profiles.get_public method."""

    @pytest.mark.asyncio
    async def test_returns_profile_light(self):
        """Should return ProfileLight instance."""
        mock_user_data = {"pk": "123456", "username": "testuser", "profile_pic_url": "http://example.com/pic.jpg"}

        with patch("easyinsta.modules.profiles.fetch_profile_by_id_no_auth", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_user_data
            profiles = Profiles()
            result = await profiles.get_public("123456")

        assert isinstance(result, ProfileLight)
        assert result.id == "123456"
        assert result.username == "testuser"

    @pytest.mark.asyncio
    async def test_calls_fetch_with_profile_id(self):
        """Should call fetch function with profile ID."""
        with patch("easyinsta.modules.profiles.fetch_profile_by_id_no_auth", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = {"pk": "123456", "username": "test"}
            profiles = Profiles()
            await profiles.get_public("123456")

        mock_fetch.assert_called_once_with("123456")


class TestProfilesGet:
    """Tests for Profiles.get method."""

    @pytest.mark.asyncio
    async def test_raises_error_when_both_params_provided(self):
        """Should raise ValueError when both username and profile_id are provided."""
        profiles = Profiles()

        with pytest.raises(ValueError) as exc_info:
            await profiles.get(username="test", profile_id="123456")

        assert str(exc_info.value) == ErrorMessages.ONLY_ONE_PARAM

    @pytest.mark.asyncio
    async def test_raises_error_when_no_params_provided(self):
        """Should raise ValueError when neither username nor profile_id is provided."""
        profiles = Profiles()

        with pytest.raises(ValueError) as exc_info:
            await profiles.get()

        assert str(exc_info.value) == ErrorMessages.MISSING_PARAM

    @pytest.mark.asyncio
    async def test_fetches_by_username(self):
        """Should fetch by username when username is provided."""
        mock_user_data = {"pk": "123456", "username": "testuser"}

        with patch("easyinsta.modules.profiles.fetch_profile_by_username", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_user_data
            profiles = Profiles()
            result = await profiles.get(username="testuser")

        assert isinstance(result, Profile)
        mock_fetch.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetches_by_profile_id(self):
        """Should fetch by profile_id when profile_id is provided."""
        mock_user_data = {"pk": "123456", "username": "testuser"}

        with patch("easyinsta.modules.profiles.fetch_profile_by_id", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_user_data
            profiles = Profiles()
            result = await profiles.get(profile_id="123456")

        assert isinstance(result, Profile)
        mock_fetch.assert_called_once()

    @pytest.mark.asyncio
    async def test_returns_profile_instance(self):
        """Should return Profile instance."""
        mock_user_data = {"pk": "123456", "username": "testuser", "full_name": "Test User"}

        with patch("easyinsta.modules.profiles.fetch_profile_by_username", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_user_data
            profiles = Profiles()
            result = await profiles.get(username="testuser")

        assert isinstance(result, Profile)
        assert result.id == "123456"
        assert result.username == "testuser"
