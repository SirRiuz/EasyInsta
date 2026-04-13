"""Tests for Account module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from easyinsta.constants import Endpoints
from easyinsta.exceptions import AuthRequiredError
from easyinsta.models import Account as AccountModel
from easyinsta.modules.account import Account
from easyinsta.modules.auth import Auth


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


@pytest.fixture
def mock_account_response():
    """Create a mock API response for current user."""
    return {
        "user": {
            "pk": 123456789,
            "fbid_v2": "17841400000000000",
            "username": "testuser",
            "full_name": "Test User",
            "biography": "This is my bio",
            "profile_pic_url": "https://example.com/pic.jpg",
            "hd_profile_pic_url_info": {"url": "https://example.com/pic_hd.jpg"},
            "is_private": False,
            "is_verified": True,
            "is_business": False,
            "follower_count": 1000,
            "following_count": 500,
            "media_count": 50,
            "phone_number": "+1234567890",
            "email": "test@example.com",
            "birthday": "1990-01-01",
            "gender": 1,
            "external_url": "https://example.com",
        }
    }


class TestAccountInfo:
    """Tests for Account.account_info method."""

    @pytest.mark.asyncio
    async def test_returns_account_model(self, mock_auth, mock_account_response):
        """Should return Account model instance."""
        with patch("easyinsta.modules.account.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = mock_account_response
            account = Account(mock_auth)
            result = await account.account_info()

        assert isinstance(result, AccountModel)

    @pytest.mark.asyncio
    async def test_returns_correct_user_data(self, mock_auth, mock_account_response):
        """Should return correct user data from API response."""
        with patch("easyinsta.modules.account.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = mock_account_response
            account = Account(mock_auth)
            result = await account.account_info()

        assert result.id == "123456789"
        assert result.username == "testuser"
        assert result.full_name == "Test User"
        assert result.biography == "This is my bio"
        assert result.email == "test@example.com"
        assert result.phone_number == "+1234567890"
        assert result.is_verified is True
        assert result.follower_count == 1000

    @pytest.mark.asyncio
    async def test_calls_api_with_correct_params(self, mock_auth, mock_account_response):
        """Should call api_call with correct endpoint and method."""
        with patch("easyinsta.modules.account.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = mock_account_response
            account = Account(mock_auth)
            await account.account_info()

        mock_api.assert_called_once_with(
            Endpoints.CURRENT_USER,
            method="GET",
            headers={"Authorization": "Bearer IGT:2:test_token"},
        )

    @pytest.mark.asyncio
    async def test_raises_auth_required_when_not_authenticated(self, mock_auth_unauthenticated):
        """Should raise AuthRequiredError when not authenticated."""
        account = Account(mock_auth_unauthenticated)

        with pytest.raises(AuthRequiredError):
            await account.account_info()

    @pytest.mark.asyncio
    async def test_handles_empty_user_response(self, mock_auth):
        """Should handle empty user object in response."""
        with patch("easyinsta.modules.account.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"user": {}}
            account = Account(mock_auth)
            result = await account.account_info()

        assert result.id == ""
        assert result.username == ""
        assert result.email == ""

    @pytest.mark.asyncio
    async def test_handles_missing_user_key(self, mock_auth):
        """Should handle missing user key in response."""
        with patch("easyinsta.modules.account.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {}
            account = Account(mock_auth)
            result = await account.account_info()

        assert result.id == ""
        assert result.username == ""


class TestAccountModel:
    """Tests for Account model attributes."""

    def test_repr(self, mock_account_response):
        """Should have correct string representation."""
        account = AccountModel(mock_account_response["user"])
        assert repr(account) == "Account(id='123456789', username='testuser')"

    def test_raw_property(self, mock_account_response):
        """Should expose raw API data."""
        account = AccountModel(mock_account_response["user"])
        assert account.raw == mock_account_response["user"]

    def test_profile_pic_hd_url(self, mock_account_response):
        """Should extract HD profile pic URL."""
        account = AccountModel(mock_account_response["user"])
        assert account.profile_pic_url_hd == "https://example.com/pic_hd.jpg"

    def test_default_values(self):
        """Should use default values for missing fields."""
        account = AccountModel({})
        assert account.id == ""
        assert account.username == ""
        assert account.is_private is False
        assert account.follower_count == 0
        assert account.gender == 0


class TestSetPublic:
    """Tests for Account.set_public method."""

    @pytest.mark.asyncio
    async def test_returns_true_on_success(self, mock_auth):
        """Should return True when set_public is successful."""
        with patch("easyinsta.modules.account.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"status": "ok"}
            account = Account(mock_auth)
            result = await account.set_public()

        assert result is True

    @pytest.mark.asyncio
    async def test_calls_api_with_correct_params(self, mock_auth):
        """Should call api_call with correct endpoint and method."""
        with patch("easyinsta.modules.account.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"status": "ok"}
            account = Account(mock_auth)
            await account.set_public()

        mock_api.assert_called_once_with(
            Endpoints.SET_PUBLIC,
            method="POST",
            headers={"Authorization": "Bearer IGT:2:test_token"},
        )

    @pytest.mark.asyncio
    async def test_raises_auth_required_when_not_authenticated(self, mock_auth_unauthenticated):
        """Should raise AuthRequiredError when not authenticated."""
        account = Account(mock_auth_unauthenticated)

        with pytest.raises(AuthRequiredError):
            await account.set_public()


class TestSetPrivate:
    """Tests for Account.set_private method."""

    @pytest.mark.asyncio
    async def test_returns_true_on_success(self, mock_auth):
        """Should return True when set_private is successful."""
        with patch("easyinsta.modules.account.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"status": "ok"}
            account = Account(mock_auth)
            result = await account.set_private()

        assert result is True

    @pytest.mark.asyncio
    async def test_calls_api_with_correct_params(self, mock_auth):
        """Should call api_call with correct endpoint and method."""
        with patch("easyinsta.modules.account.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"status": "ok"}
            account = Account(mock_auth)
            await account.set_private()

        mock_api.assert_called_once_with(
            Endpoints.SET_PRIVATE,
            method="POST",
            headers={"Authorization": "Bearer IGT:2:test_token"},
        )

    @pytest.mark.asyncio
    async def test_raises_auth_required_when_not_authenticated(self, mock_auth_unauthenticated):
        """Should raise AuthRequiredError when not authenticated."""
        account = Account(mock_auth_unauthenticated)

        with pytest.raises(AuthRequiredError):
            await account.set_private()
