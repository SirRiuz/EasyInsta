"""Tests for Profiles module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from easyinsta.modules.auth import Auth
from easyinsta.constants import ErrorMessages
from easyinsta.exceptions import AuthRequiredError
from easyinsta.models import Profile, ProfileLight
from easyinsta.modules.profiles import Profiles


@pytest.fixture
def mock_auth():
    """Create a mock Auth instance with authentication."""
    auth = MagicMock(spec=Auth)
    auth.headers = {"Authorization": "Bearer IGT:2:test_token"}
    auth.is_authenticated = True
    return auth


@pytest.fixture
def mock_auth_unauthenticated():
    """Create a mock Auth instance without authentication."""
    auth = MagicMock(spec=Auth)
    auth.headers = {}
    auth.is_authenticated = False
    return auth


class TestProfilesGetPublic:
    """Tests for Profiles.get_public method."""

    @pytest.mark.asyncio
    async def test_returns_profile_light(self, mock_auth):
        """Should return ProfileLight instance."""
        mock_user_data = {"pk": "123456", "username": "testuser", "profile_pic_url": "http://example.com/pic.jpg"}

        with patch("easyinsta.modules.profiles.fetch_profile_by_id_no_auth", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_user_data
            profiles = Profiles(mock_auth)
            result = await profiles.get_public("123456")

        assert isinstance(result, ProfileLight)
        assert result.id == "123456"
        assert result.username == "testuser"

    @pytest.mark.asyncio
    async def test_calls_fetch_with_profile_id(self, mock_auth):
        """Should call fetch function with profile ID."""
        with patch("easyinsta.modules.profiles.fetch_profile_by_id_no_auth", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = {"pk": "123456", "username": "test"}
            profiles = Profiles(mock_auth)
            await profiles.get_public("123456")

        mock_fetch.assert_called_once_with("123456")


class TestProfilesGet:
    """Tests for Profiles.get method."""

    @pytest.mark.asyncio
    async def test_raises_error_when_both_params_provided(self, mock_auth):
        """Should raise ValueError when both username and profile_id are provided."""
        profiles = Profiles(mock_auth)

        with pytest.raises(ValueError) as exc_info:
            await profiles.get(username="test", profile_id="123456")

        assert str(exc_info.value) == ErrorMessages.ONLY_ONE_PARAM

    @pytest.mark.asyncio
    async def test_raises_error_when_no_params_provided(self, mock_auth):
        """Should raise ValueError when neither username nor profile_id is provided."""
        profiles = Profiles(mock_auth)

        with pytest.raises(ValueError) as exc_info:
            await profiles.get()

        assert str(exc_info.value) == ErrorMessages.MISSING_PARAM

    @pytest.mark.asyncio
    async def test_fetches_by_username(self, mock_auth):
        """Should fetch by username when username is provided."""
        mock_user_data = {"pk": "123456", "username": "testuser"}

        with patch("easyinsta.modules.profiles.fetch_profile_by_username", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_user_data
            profiles = Profiles(mock_auth)
            result = await profiles.get(username="testuser")

        assert isinstance(result, Profile)
        mock_fetch.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetches_by_profile_id(self, mock_auth):
        """Should fetch by profile_id when profile_id is provided."""
        mock_user_data = {"pk": "123456", "username": "testuser"}

        with patch("easyinsta.modules.profiles.fetch_profile_by_id", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_user_data
            profiles = Profiles(mock_auth)
            result = await profiles.get(profile_id="123456")

        assert isinstance(result, Profile)
        mock_fetch.assert_called_once()

    @pytest.mark.asyncio
    async def test_returns_profile_instance(self, mock_auth):
        """Should return Profile instance."""
        mock_user_data = {"pk": "123456", "username": "testuser", "full_name": "Test User"}

        with patch("easyinsta.modules.profiles.fetch_profile_by_username", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_user_data
            profiles = Profiles(mock_auth)
            result = await profiles.get(username="testuser")

        assert isinstance(result, Profile)
        assert result.id == "123456"
        assert result.username == "testuser"

    @pytest.mark.asyncio
    async def test_uses_auth_headers(self, mock_auth):
        """Should use auth headers from Auth instance."""
        mock_user_data = {"pk": "123456", "username": "testuser"}

        with patch("easyinsta.modules.profiles.fetch_profile_by_username", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_user_data
            profiles = Profiles(mock_auth)
            await profiles.get(username="testuser")

        mock_fetch.assert_called_once_with("testuser", {"Authorization": "Bearer IGT:2:test_token"})

    @pytest.mark.asyncio
    async def test_raises_auth_required_when_not_authenticated(self, mock_auth_unauthenticated):
        """Should raise AuthRequiredError when not authenticated."""
        profiles = Profiles(mock_auth_unauthenticated)

        with pytest.raises(AuthRequiredError):
            await profiles.get(username="testuser")
