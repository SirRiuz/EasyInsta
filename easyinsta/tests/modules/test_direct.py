"""Tests for Direct module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from easyinsta.modules.auth import Auth
from easyinsta.exceptions import AuthRequiredError
from easyinsta.models import Inbox
from easyinsta.modules.direct import Direct


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
def mock_inbox_response():
    """Create a mock inbox API response."""
    return {
        "inbox": {
            "threads": [
                {
                    "thread_id": "thread_1",
                    "thread_title": "Test Thread",
                    "last_activity_at": 1234567890,
                    "marked_as_unread": False,
                    "users": [{"username": "user1", "full_name": "User One"}],
                },
                {
                    "thread_id": "thread_2",
                    "thread_title": "",
                    "last_activity_at": 1234567891,
                    "marked_as_unread": True,
                    "users": [{"username": "user2", "full_name": "User Two"}],
                },
            ],
            "has_older": True,
            "oldest_cursor": "cursor_page_1",
        }
    }


class TestDirectGetInbox:
    """Tests for Direct.get_inbox method."""

    @pytest.mark.asyncio
    async def test_returns_inbox_instance(self, mock_auth, mock_inbox_response):
        """Should return Inbox instance."""
        with patch("easyinsta.modules.direct.fetch_inbox", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_inbox_response
            direct = Direct(mock_auth)
            result = await direct.get_inbox()

        assert isinstance(result, Inbox)

    @pytest.mark.asyncio
    async def test_returns_threads(self, mock_auth, mock_inbox_response):
        """Should return inbox with threads."""
        with patch("easyinsta.modules.direct.fetch_inbox", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_inbox_response
            direct = Direct(mock_auth)
            result = await direct.get_inbox()

        assert len(result.threads) == 2
        assert result.threads[0].thread_id == "thread_1"
        assert result.threads[1].thread_id == "thread_2"

    @pytest.mark.asyncio
    async def test_raises_auth_required_when_not_authenticated(self, mock_auth_unauthenticated):
        """Should raise AuthRequiredError when not authenticated."""
        direct = Direct(mock_auth_unauthenticated)

        with pytest.raises(AuthRequiredError):
            await direct.get_inbox()

    @pytest.mark.asyncio
    async def test_raises_value_error_for_invalid_page(self, mock_auth):
        """Should raise ValueError when page is less than 1."""
        direct = Direct(mock_auth)

        with pytest.raises(ValueError) as exc_info:
            await direct.get_inbox(page=0)

        assert "Page number must be at least 1" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_calls_fetch_with_credentials(self, mock_auth, mock_inbox_response):
        """Should call fetch_inbox with auth credentials."""
        with patch("easyinsta.modules.direct.fetch_inbox", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_inbox_response
            direct = Direct(mock_auth)
            await direct.get_inbox()

        mock_fetch.assert_called_once_with(
            {"Authorization": "Bearer IGT:2:test_token"},
            cursor=None,
        )

    @pytest.mark.asyncio
    async def test_stores_cursor_for_pagination(self, mock_auth, mock_inbox_response):
        """Should store cursor for next page pagination."""
        with patch("easyinsta.modules.direct.fetch_inbox", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_inbox_response
            direct = Direct(mock_auth)
            await direct.get_inbox(page=1)

        assert direct._cursors[1] == "cursor_page_1"

    @pytest.mark.asyncio
    async def test_uses_cursor_for_page_2(self, mock_auth):
        """Should use stored cursor when fetching page 2."""
        page1_response = {
            "inbox": {
                "threads": [{"thread_id": "t1", "users": []}],
                "has_older": True,
                "oldest_cursor": "cursor_for_page_2",
            }
        }
        page2_response = {
            "inbox": {
                "threads": [{"thread_id": "t2", "users": []}],
                "has_older": False,
                "oldest_cursor": "",
            }
        }

        with patch("easyinsta.modules.direct.fetch_inbox", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.side_effect = [page1_response, page2_response]
            direct = Direct(mock_auth)

            await direct.get_inbox(page=1)
            await direct.get_inbox(page=2)

        calls = mock_fetch.call_args_list
        assert calls[1][1]["cursor"] == "cursor_for_page_2"

    @pytest.mark.asyncio
    async def test_fetches_previous_pages_when_jumping(self, mock_auth):
        """Should fetch previous pages to get cursor when jumping to later page."""
        page1_response = {
            "inbox": {
                "threads": [{"thread_id": "t1", "users": []}],
                "has_older": True,
                "oldest_cursor": "cursor_1",
            }
        }
        page2_response = {
            "inbox": {
                "threads": [{"thread_id": "t2", "users": []}],
                "has_older": True,
                "oldest_cursor": "cursor_2",
            }
        }
        page3_response = {
            "inbox": {
                "threads": [{"thread_id": "t3", "users": []}],
                "has_older": False,
                "oldest_cursor": "",
            }
        }

        with patch("easyinsta.modules.direct.fetch_inbox", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.side_effect = [page1_response, page2_response, page3_response]
            direct = Direct(mock_auth)

            result = await direct.get_inbox(page=3)

        assert mock_fetch.call_count == 3
        assert result.threads[0].thread_id == "t3"

    @pytest.mark.asyncio
    async def test_skips_cached_cursors_in_loop(self, mock_auth):
        """Should skip fetching pages with already cached cursors in the loop."""
        page1_response = {
            "inbox": {
                "threads": [{"thread_id": "t1", "users": []}],
                "has_older": True,
                "oldest_cursor": "cursor_1",
            }
        }
        page3_response = {
            "inbox": {
                "threads": [{"thread_id": "t3", "users": []}],
                "has_older": True,
                "oldest_cursor": "cursor_3",
            }
        }
        page4_response = {
            "inbox": {
                "threads": [{"thread_id": "t4", "users": []}],
                "has_older": False,
                "oldest_cursor": "",
            }
        }

        with patch("easyinsta.modules.direct.fetch_inbox", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.side_effect = [page1_response, page3_response, page4_response]
            direct = Direct(mock_auth)

            # Pre-cache cursor for page 2 (simulating it was fetched before)
            direct._cursors[2] = "cursor_2"

            result = await direct.get_inbox(page=4)

        # Should fetch page 1, skip page 2 (cached), fetch page 3 and page 4
        assert mock_fetch.call_count == 3
        assert result.threads[0].thread_id == "t4"
