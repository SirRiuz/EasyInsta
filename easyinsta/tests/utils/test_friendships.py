"""Tests for friendships utilities."""

from unittest.mock import AsyncMock, patch

import pytest

from easyinsta.utils.friendships import (
    add_close_friend,
    block_user,
    follow_user,
    remove_close_friend,
    unblock_user,
    unfollow_user,
)


class TestFollowUser:
    """Tests for follow_user function."""

    @pytest.mark.asyncio
    async def test_calls_api_with_correct_params(self):
        """Should call api_call with correct endpoint and body."""
        with patch("easyinsta.utils.friendships.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"status": "ok"}
            headers = {"Authorization": "Bearer token"}

            result = await follow_user("123456", headers)

        mock_api.assert_called_once_with(
            "/api/v1/friendships/create/123456/",
            method="POST",
            body={"user_id": "123456"},
            headers=headers,
        )
        assert result == {"status": "ok"}


class TestUnfollowUser:
    """Tests for unfollow_user function."""

    @pytest.mark.asyncio
    async def test_calls_api_with_correct_params(self):
        """Should call api_call with correct endpoint and body."""
        with patch("easyinsta.utils.friendships.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"status": "ok"}
            headers = {"Authorization": "Bearer token"}

            result = await unfollow_user("123456", headers)

        mock_api.assert_called_once_with(
            "/api/v1/friendships/destroy/123456/",
            method="POST",
            body={"user_id": "123456"},
            headers=headers,
        )
        assert result == {"status": "ok"}


class TestAddCloseFriend:
    """Tests for add_close_friend function."""

    @pytest.mark.asyncio
    async def test_calls_api_with_correct_params(self):
        """Should call api_call with correct endpoint and body."""
        with patch("easyinsta.utils.friendships.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"status": "ok"}
            headers = {"Authorization": "Bearer token"}

            result = await add_close_friend("123456", headers)

        mock_api.assert_called_once_with(
            "/api/v1/friendships/set_besties/",
            method="POST",
            body={"add": '["123456"]', "remove": '[]'},
            headers=headers,
        )
        assert result == {"status": "ok"}


class TestRemoveCloseFriend:
    """Tests for remove_close_friend function."""

    @pytest.mark.asyncio
    async def test_calls_api_with_correct_params(self):
        """Should call api_call with correct endpoint and body."""
        with patch("easyinsta.utils.friendships.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"status": "ok"}
            headers = {"Authorization": "Bearer token"}

            result = await remove_close_friend("123456", headers)

        mock_api.assert_called_once_with(
            "/api/v1/friendships/set_besties/",
            method="POST",
            body={"add": '[]', "remove": '["123456"]'},
            headers=headers,
        )
        assert result == {"status": "ok"}


class TestBlockUser:
    """Tests for block_user function."""

    @pytest.mark.asyncio
    async def test_calls_api_with_correct_params(self):
        """Should call api_call with correct endpoint and body."""
        with patch("easyinsta.utils.friendships.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"status": "ok"}
            headers = {"Authorization": "Bearer token"}

            result = await block_user("123456", headers)

        mock_api.assert_called_once_with(
            "/api/v1/friendships/block/123456/",
            method="POST",
            body={"user_id": "123456", "surface": "profile"},
            headers=headers,
        )
        assert result == {"status": "ok"}


class TestUnblockUser:
    """Tests for unblock_user function."""

    @pytest.mark.asyncio
    async def test_calls_api_with_correct_params(self):
        """Should call api_call with correct endpoint and body."""
        with patch("easyinsta.utils.friendships.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"status": "ok"}
            headers = {"Authorization": "Bearer token"}

            result = await unblock_user("123456", headers)

        mock_api.assert_called_once_with(
            "/api/v1/friendships/unblock/123456/",
            method="POST",
            body={"user_id": "123456", "container_module": "profile"},
            headers=headers,
        )
        assert result == {"status": "ok"}
