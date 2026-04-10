"""Tests for Profiles module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from easyinsta.modules.auth import Auth
from easyinsta.constants import ErrorMessages
from easyinsta.exceptions import AuthRequiredError, InvalidFormatError, MissingFieldError
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


class TestUserIdFromUsername:
    """Tests for Profiles.user_id_from_username method."""

    @pytest.mark.asyncio
    async def test_returns_user_id_as_int(self, mock_auth):
        """Should return user ID as integer."""
        mock_user_data = {"pk": "314216", "username": "zuck"}

        with patch("easyinsta.modules.profiles.fetch_profile_by_username", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_user_data
            profiles = Profiles(mock_auth)
            result = await profiles.user_id_from_username("zuck")

        assert result == 314216
        assert isinstance(result, int)

    @pytest.mark.asyncio
    async def test_calls_fetch_with_username_and_headers(self, mock_auth):
        """Should call fetch function with username and auth headers."""
        mock_user_data = {"pk": "123456", "username": "testuser"}

        with patch("easyinsta.modules.profiles.fetch_profile_by_username", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_user_data
            profiles = Profiles(mock_auth)
            await profiles.user_id_from_username("testuser")

        mock_fetch.assert_called_once_with("testuser", {"Authorization": "Bearer IGT:2:test_token"})

    @pytest.mark.asyncio
    async def test_raises_auth_required_when_not_authenticated(self, mock_auth_unauthenticated):
        """Should raise AuthRequiredError when not authenticated."""
        profiles = Profiles(mock_auth_unauthenticated)

        with pytest.raises(AuthRequiredError):
            await profiles.user_id_from_username("testuser")


class TestUsernameFromUserId:
    """Tests for Profiles.username_from_user_id method."""

    @pytest.mark.asyncio
    async def test_returns_username_as_string(self, mock_auth):
        """Should return username as string."""
        mock_user_data = {"pk": "314216", "username": "zuck"}

        with patch("easyinsta.modules.profiles.fetch_profile_by_id", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_user_data
            profiles = Profiles(mock_auth)
            result = await profiles.username_from_user_id("314216")

        assert result == "zuck"
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_calls_fetch_with_user_id_and_headers(self, mock_auth):
        """Should call fetch function with user ID and auth headers."""
        mock_user_data = {"pk": "123456", "username": "testuser"}

        with patch("easyinsta.modules.profiles.fetch_profile_by_id", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_user_data
            profiles = Profiles(mock_auth)
            await profiles.username_from_user_id("123456")

        mock_fetch.assert_called_once_with("123456", {"Authorization": "Bearer IGT:2:test_token"})

    @pytest.mark.asyncio
    async def test_raises_auth_required_when_not_authenticated(self, mock_auth_unauthenticated):
        """Should raise AuthRequiredError when not authenticated."""
        profiles = Profiles(mock_auth_unauthenticated)

        with pytest.raises(AuthRequiredError):
            await profiles.username_from_user_id("123456")


class TestProfilesFollow:
    """Tests for Profiles.follow method."""

    @pytest.mark.asyncio
    async def test_returns_true_on_success(self, mock_auth):
        """Should return True when follow is successful."""
        with patch("easyinsta.modules.profiles.follow_user", new_callable=AsyncMock) as mock_follow:
            mock_follow.return_value = {"status": "ok"}
            profiles = Profiles(mock_auth)
            result = await profiles.follow("314216")

        assert result is True

    @pytest.mark.asyncio
    async def test_calls_follow_user_with_correct_params(self, mock_auth):
        """Should call follow_user with user_id and headers."""
        with patch("easyinsta.modules.profiles.follow_user", new_callable=AsyncMock) as mock_follow:
            mock_follow.return_value = {"status": "ok"}
            profiles = Profiles(mock_auth)
            await profiles.follow("314216")

        mock_follow.assert_called_once_with("314216", {"Authorization": "Bearer IGT:2:test_token"})

    @pytest.mark.asyncio
    async def test_raises_auth_required_when_not_authenticated(self, mock_auth_unauthenticated):
        """Should raise AuthRequiredError when not authenticated."""
        profiles = Profiles(mock_auth_unauthenticated)

        with pytest.raises(AuthRequiredError):
            await profiles.follow("314216")


class TestProfilesUnfollow:
    """Tests for Profiles.unfollow method."""

    @pytest.mark.asyncio
    async def test_returns_true_on_success(self, mock_auth):
        """Should return True when unfollow is successful."""
        with patch("easyinsta.modules.profiles.unfollow_user", new_callable=AsyncMock) as mock_unfollow:
            mock_unfollow.return_value = {"status": "ok"}
            profiles = Profiles(mock_auth)
            result = await profiles.unfollow("314216")

        assert result is True

    @pytest.mark.asyncio
    async def test_calls_unfollow_user_with_correct_params(self, mock_auth):
        """Should call unfollow_user with user_id and headers."""
        with patch("easyinsta.modules.profiles.unfollow_user", new_callable=AsyncMock) as mock_unfollow:
            mock_unfollow.return_value = {"status": "ok"}
            profiles = Profiles(mock_auth)
            await profiles.unfollow("314216")

        mock_unfollow.assert_called_once_with("314216", {"Authorization": "Bearer IGT:2:test_token"})

    @pytest.mark.asyncio
    async def test_raises_auth_required_when_not_authenticated(self, mock_auth_unauthenticated):
        """Should raise AuthRequiredError when not authenticated."""
        profiles = Profiles(mock_auth_unauthenticated)

        with pytest.raises(AuthRequiredError):
            await profiles.unfollow("314216")


class TestExistsByUsername:
    """Tests for Profiles.exists_by_username method."""

    @pytest.mark.asyncio
    async def test_returns_true_when_account_exists(self, mock_auth):
        """Should return True when account exists (username not available)."""
        with patch("easyinsta.modules.profiles.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"available": False}
            profiles = Profiles(mock_auth)
            result = await profiles.exists_by_username("zuck")

        assert result is True

    @pytest.mark.asyncio
    async def test_returns_false_when_account_does_not_exist(self, mock_auth):
        """Should return False when account does not exist (username available)."""
        with patch("easyinsta.modules.profiles.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"available": True}
            profiles = Profiles(mock_auth)
            result = await profiles.exists_by_username("nonexistent_user_12345")

        assert result is False

    @pytest.mark.asyncio
    async def test_raises_missing_field_error(self, mock_auth):
        """Should raise MissingFieldError when response lacks 'available' field."""
        with patch("easyinsta.modules.profiles.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {}
            profiles = Profiles(mock_auth)

            with pytest.raises(MissingFieldError) as exc_info:
                await profiles.exists_by_username("testuser")

        assert exc_info.value.field == "available"


class TestExistsByEmail:
    """Tests for Profiles.exists_by_email method."""

    @pytest.mark.asyncio
    async def test_returns_true_when_account_exists(self, mock_auth):
        """Should return True when account exists (email not available)."""
        with patch("easyinsta.modules.profiles.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"valid": True, "available": False}
            profiles = Profiles(mock_auth)
            result = await profiles.exists_by_email("taken@example.com")

        assert result is True

    @pytest.mark.asyncio
    async def test_returns_false_when_account_does_not_exist(self, mock_auth):
        """Should return False when account does not exist (email available)."""
        with patch("easyinsta.modules.profiles.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"valid": True, "available": True}
            profiles = Profiles(mock_auth)
            result = await profiles.exists_by_email("available@example.com")

        assert result is False

    @pytest.mark.asyncio
    async def test_raises_missing_field_error_for_valid(self, mock_auth):
        """Should raise MissingFieldError when response lacks 'valid' field."""
        with patch("easyinsta.modules.profiles.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {}
            profiles = Profiles(mock_auth)

            with pytest.raises(MissingFieldError) as exc_info:
                await profiles.exists_by_email("test@example.com")

        assert exc_info.value.field == "valid"

    @pytest.mark.asyncio
    async def test_raises_invalid_format_error(self, mock_auth):
        """Should raise InvalidFormatError when email format is invalid."""
        with patch("easyinsta.modules.profiles.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"valid": False}
            profiles = Profiles(mock_auth)

            with pytest.raises(InvalidFormatError) as exc_info:
                await profiles.exists_by_email("invalid-email")

        assert exc_info.value.field == "email"

    @pytest.mark.asyncio
    async def test_raises_missing_field_error_for_available(self, mock_auth):
        """Should raise MissingFieldError when response lacks 'available' field."""
        with patch("easyinsta.modules.profiles.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"valid": True}
            profiles = Profiles(mock_auth)

            with pytest.raises(MissingFieldError) as exc_info:
                await profiles.exists_by_email("test@example.com")

        assert exc_info.value.field == "available"


class TestAddToCloseFriends:
    """Tests for Profiles.add_to_close_friends method."""

    @pytest.mark.asyncio
    async def test_returns_true_on_success(self, mock_auth):
        """Should return True when adding to close friends is successful."""
        with patch("easyinsta.modules.profiles.add_close_friend", new_callable=AsyncMock) as mock_add:
            mock_add.return_value = {"status": "ok"}
            profiles = Profiles(mock_auth)
            result = await profiles.add_to_close_friends("314216")

        assert result is True

    @pytest.mark.asyncio
    async def test_calls_add_close_friend_with_correct_params(self, mock_auth):
        """Should call add_close_friend with user_id and headers."""
        with patch("easyinsta.modules.profiles.add_close_friend", new_callable=AsyncMock) as mock_add:
            mock_add.return_value = {"status": "ok"}
            profiles = Profiles(mock_auth)
            await profiles.add_to_close_friends("314216")

        mock_add.assert_called_once_with("314216", {"Authorization": "Bearer IGT:2:test_token"})

    @pytest.mark.asyncio
    async def test_raises_auth_required_when_not_authenticated(self, mock_auth_unauthenticated):
        """Should raise AuthRequiredError when not authenticated."""
        profiles = Profiles(mock_auth_unauthenticated)

        with pytest.raises(AuthRequiredError):
            await profiles.add_to_close_friends("314216")


class TestRemoveFromCloseFriends:
    """Tests for Profiles.remove_from_close_friends method."""

    @pytest.mark.asyncio
    async def test_returns_true_on_success(self, mock_auth):
        """Should return True when removing from close friends is successful."""
        with patch("easyinsta.modules.profiles.remove_close_friend", new_callable=AsyncMock) as mock_remove:
            mock_remove.return_value = {"status": "ok"}
            profiles = Profiles(mock_auth)
            result = await profiles.remove_from_close_friends("314216")

        assert result is True

    @pytest.mark.asyncio
    async def test_calls_remove_close_friend_with_correct_params(self, mock_auth):
        """Should call remove_close_friend with user_id and headers."""
        with patch("easyinsta.modules.profiles.remove_close_friend", new_callable=AsyncMock) as mock_remove:
            mock_remove.return_value = {"status": "ok"}
            profiles = Profiles(mock_auth)
            await profiles.remove_from_close_friends("314216")

        mock_remove.assert_called_once_with("314216", {"Authorization": "Bearer IGT:2:test_token"})

    @pytest.mark.asyncio
    async def test_raises_auth_required_when_not_authenticated(self, mock_auth_unauthenticated):
        """Should raise AuthRequiredError when not authenticated."""
        profiles = Profiles(mock_auth_unauthenticated)

        with pytest.raises(AuthRequiredError):
            await profiles.remove_from_close_friends("314216")


class TestBlock:
    """Tests for Profiles.block method."""

    @pytest.mark.asyncio
    async def test_returns_true_on_success(self, mock_auth):
        """Should return True when blocking is successful."""
        with patch("easyinsta.modules.profiles.block_user", new_callable=AsyncMock) as mock_block:
            mock_block.return_value = {"status": "ok"}
            profiles = Profiles(mock_auth)
            result = await profiles.block("314216")

        assert result is True

    @pytest.mark.asyncio
    async def test_calls_block_user_with_correct_params(self, mock_auth):
        """Should call block_user with user_id and headers."""
        with patch("easyinsta.modules.profiles.block_user", new_callable=AsyncMock) as mock_block:
            mock_block.return_value = {"status": "ok"}
            profiles = Profiles(mock_auth)
            await profiles.block("314216")

        mock_block.assert_called_once_with("314216", {"Authorization": "Bearer IGT:2:test_token"})

    @pytest.mark.asyncio
    async def test_raises_auth_required_when_not_authenticated(self, mock_auth_unauthenticated):
        """Should raise AuthRequiredError when not authenticated."""
        profiles = Profiles(mock_auth_unauthenticated)

        with pytest.raises(AuthRequiredError):
            await profiles.block("314216")


class TestUnblock:
    """Tests for Profiles.unblock method."""

    @pytest.mark.asyncio
    async def test_returns_true_on_success(self, mock_auth):
        """Should return True when unblocking is successful."""
        with patch("easyinsta.modules.profiles.unblock_user", new_callable=AsyncMock) as mock_unblock:
            mock_unblock.return_value = {"status": "ok"}
            profiles = Profiles(mock_auth)
            result = await profiles.unblock("314216")

        assert result is True

    @pytest.mark.asyncio
    async def test_calls_unblock_user_with_correct_params(self, mock_auth):
        """Should call unblock_user with user_id and headers."""
        with patch("easyinsta.modules.profiles.unblock_user", new_callable=AsyncMock) as mock_unblock:
            mock_unblock.return_value = {"status": "ok"}
            profiles = Profiles(mock_auth)
            await profiles.unblock("314216")

        mock_unblock.assert_called_once_with("314216", {"Authorization": "Bearer IGT:2:test_token"})

    @pytest.mark.asyncio
    async def test_raises_auth_required_when_not_authenticated(self, mock_auth_unauthenticated):
        """Should raise AuthRequiredError when not authenticated."""
        profiles = Profiles(mock_auth_unauthenticated)

        with pytest.raises(AuthRequiredError):
            await profiles.unblock("314216")
