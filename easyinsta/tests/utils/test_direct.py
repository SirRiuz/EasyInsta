"""Tests for direct message utilities."""

from unittest.mock import AsyncMock, patch

import pytest

from easyinsta.utils.direct import fetch_inbox


class TestFetchInbox:
    """Tests for fetch_inbox function."""

    @pytest.mark.asyncio
    async def test_calls_api_with_correct_path(self):
        """Should call api_call with correct endpoint."""
        with patch("easyinsta.utils.direct.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"inbox": {"threads": []}}
            await fetch_inbox({"Authorization": "Bearer token"})

        call_args = mock_api.call_args
        assert "/api/v1/direct_v2/inbox/" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_includes_default_params(self):
        """Should include default query parameters."""
        with patch("easyinsta.utils.direct.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"inbox": {"threads": []}}
            await fetch_inbox({"Authorization": "Bearer token"})

        call_args = mock_api.call_args
        path = call_args[0][0]
        assert "visual_message_return_type=unseen" in path
        assert "selected_filter=unread" in path
        assert "limit=20" in path

    @pytest.mark.asyncio
    async def test_includes_cursor_when_provided(self):
        """Should include cursor in query params when provided."""
        with patch("easyinsta.utils.direct.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"inbox": {"threads": []}}
            await fetch_inbox({"Authorization": "Bearer token"}, cursor="abc123")

        call_args = mock_api.call_args
        path = call_args[0][0]
        assert "cursor=abc123" in path

    @pytest.mark.asyncio
    async def test_excludes_cursor_when_not_provided(self):
        """Should not include cursor when not provided."""
        with patch("easyinsta.utils.direct.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"inbox": {"threads": []}}
            await fetch_inbox({"Authorization": "Bearer token"})

        call_args = mock_api.call_args
        path = call_args[0][0]
        assert "cursor=" not in path

    @pytest.mark.asyncio
    async def test_uses_custom_limit(self):
        """Should use custom limit when provided."""
        with patch("easyinsta.utils.direct.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"inbox": {"threads": []}}
            await fetch_inbox({"Authorization": "Bearer token"}, limit=50)

        call_args = mock_api.call_args
        path = call_args[0][0]
        assert "limit=50" in path

    @pytest.mark.asyncio
    async def test_uses_custom_filter_type(self):
        """Should use custom filter_type when provided."""
        with patch("easyinsta.utils.direct.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"inbox": {"threads": []}}
            await fetch_inbox({"Authorization": "Bearer token"}, filter_type="all")

        call_args = mock_api.call_args
        path = call_args[0][0]
        assert "selected_filter=all" in path

    @pytest.mark.asyncio
    async def test_passes_headers(self):
        """Should pass headers to api_call."""
        headers = {"Authorization": "Bearer token"}

        with patch("easyinsta.utils.direct.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"inbox": {"threads": []}}
            await fetch_inbox(headers)

        call_args = mock_api.call_args
        assert call_args[1]["headers"] == headers

    @pytest.mark.asyncio
    async def test_uses_get_method(self):
        """Should use GET method."""
        with patch("easyinsta.utils.direct.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {"inbox": {"threads": []}}
            await fetch_inbox({"Authorization": "Bearer token"})

        call_args = mock_api.call_args
        assert call_args[1]["method"] == "GET"

    @pytest.mark.asyncio
    async def test_returns_api_response(self):
        """Should return the API response."""
        expected = {"inbox": {"threads": [{"thread_id": "1"}]}}

        with patch("easyinsta.utils.direct.api_call", new_callable=AsyncMock) as mock_api:
            mock_api.return_value = expected
            result = await fetch_inbox({"Authorization": "Bearer token"})

        assert result == expected
