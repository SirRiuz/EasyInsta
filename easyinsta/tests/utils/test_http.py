"""Tests for HTTP utilities."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from easyinsta.core.session import Session
from easyinsta.exceptions import ApiError
from easyinsta.utils.http import BASE_URL, api_call, extract_token_from_headers


def create_mock_session(status: int = 200, json_data: dict | None = None, headers: dict | None = None):
    """Helper to create a properly configured mock session."""
    mock_response = MagicMock()
    mock_response.status = status
    mock_response.json = AsyncMock(return_value=json_data or {})
    mock_response.headers = headers or {}

    mock_request_context = MagicMock()
    mock_request_context.__aenter__ = AsyncMock(return_value=mock_response)
    mock_request_context.__aexit__ = AsyncMock(return_value=None)

    mock_session = MagicMock()
    mock_session.request = MagicMock(return_value=mock_request_context)

    mock_session_context = MagicMock()
    mock_session_context.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_context.__aexit__ = AsyncMock(return_value=None)

    return mock_session_context, mock_session


class TestExtractTokenFromHeaders:
    """Tests for extract_token_from_headers function."""

    def test_returns_none_when_headers_is_none(self):
        """Should return None when headers is None."""
        assert extract_token_from_headers(None) is None

    def test_returns_none_when_no_authorization_header(self):
        """Should return None when Authorization header is missing."""
        assert extract_token_from_headers({"X-Custom": "value"}) is None

    def test_returns_none_when_authorization_not_bearer_igt2(self):
        """Should return None when Authorization is not Bearer IGT:2."""
        assert extract_token_from_headers({"Authorization": "Bearer other"}) is None

    def test_extracts_token_from_bearer_igt2(self):
        """Should extract token from Bearer IGT:2: prefix."""
        headers = {"Authorization": "Bearer IGT:2:mytoken123"}
        assert extract_token_from_headers(headers) == "mytoken123"


class TestApiCall:
    """Tests for api_call function."""

    @pytest.mark.asyncio
    async def test_successful_get_request(self):
        """Should return JSON data on successful GET request."""
        mock_session_context, _ = create_mock_session(
            status=200, json_data={"user": {"id": "123"}}
        )

        with patch(
            "easyinsta.utils.http.aiohttp.ClientSession",
            return_value=mock_session_context,
        ):
            result = await api_call("/api/v1/users/123/info/", method="GET")

        assert result["user"] == {"id": "123"}
        assert "response_context" in result

    @pytest.mark.asyncio
    async def test_successful_post_request(self):
        """Should return JSON data on successful POST request."""
        mock_session_context, _ = create_mock_session(
            status=200, json_data={"status": "ok"}
        )

        with patch(
            "easyinsta.utils.http.aiohttp.ClientSession",
            return_value=mock_session_context,
        ):
            result = await api_call(
                "/api/v1/users/check_username/", body={"username": "test"}
            )

        assert result["status"] == "ok"
        assert "response_context" in result

    @pytest.mark.asyncio
    async def test_response_context_contains_status_and_headers(self):
        """Should include status_code and headers in response_context."""
        mock_session_context, _ = create_mock_session(
            status=200,
            json_data={"status": "ok"},
            headers={"X-Custom": "value"},
        )

        with patch(
            "easyinsta.utils.http.aiohttp.ClientSession",
            return_value=mock_session_context,
        ):
            result = await api_call("/test", method="GET")

        assert result["response_context"]["status_code"] == 200
        assert result["response_context"]["headers"]["X-Custom"] == "value"

    @pytest.mark.asyncio
    async def test_raises_api_error_on_non_200_status(self):
        """Should raise ApiError when status code is not 200."""
        mock_session_context, _ = create_mock_session(status=404)

        with patch(
            "easyinsta.utils.http.aiohttp.ClientSession",
            return_value=mock_session_context,
        ):
            with pytest.raises(ApiError) as exc_info:
                await api_call("/api/v1/users/invalid/info/", method="GET")

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_raises_api_error_on_401_status(self):
        """Should raise ApiError when status code is 401."""
        mock_session_context, _ = create_mock_session(status=401)

        with patch(
            "easyinsta.utils.http.aiohttp.ClientSession",
            return_value=mock_session_context,
        ):
            with pytest.raises(ApiError) as exc_info:
                await api_call("/api/v1/users/123/info/", method="GET")

        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_includes_default_headers(self):
        """Should include default session headers in request."""
        mock_session_context, mock_session = create_mock_session(status=200)

        with patch(
            "easyinsta.utils.http.aiohttp.ClientSession",
            return_value=mock_session_context,
        ):
            await api_call("/test", method="GET")

        call_kwargs = mock_session.request.call_args
        headers = call_kwargs.kwargs["headers"]

        # Should have key Instagram headers
        assert "User-Agent" in headers
        assert "X-Ig-App-ID" in headers
        assert "X-Ig-Capabilities" in headers

    @pytest.mark.asyncio
    async def test_includes_custom_headers(self):
        """Should include custom headers in request."""
        mock_session_context, mock_session = create_mock_session(status=200)

        custom_headers = {"Authorization": "Bearer test_token"}

        with patch(
            "easyinsta.utils.http.aiohttp.ClientSession",
            return_value=mock_session_context,
        ):
            await api_call("/test", method="GET", headers=custom_headers)

        call_kwargs = mock_session.request.call_args
        headers = call_kwargs.kwargs["headers"]

        assert headers["Authorization"] == "Bearer test_token"

    @pytest.mark.asyncio
    async def test_includes_user_agent(self):
        """Should include User-Agent header in request."""
        mock_session_context, mock_session = create_mock_session(status=200)

        with patch(
            "easyinsta.utils.http.aiohttp.ClientSession",
            return_value=mock_session_context,
        ):
            await api_call("/test", method="GET")

        call_kwargs = mock_session.request.call_args
        headers = call_kwargs.kwargs["headers"]

        assert "User-Agent" in headers
        assert "Instagram" in headers["User-Agent"]

    @pytest.mark.asyncio
    async def test_constructs_correct_url(self):
        """Should construct correct full URL."""
        mock_session_context, mock_session = create_mock_session(status=200)

        with patch(
            "easyinsta.utils.http.aiohttp.ClientSession",
            return_value=mock_session_context,
        ):
            await api_call("/api/v1/users/123/info/", method="GET")

        call_args = mock_session.request.call_args
        assert call_args.args[0] == "GET"
        assert call_args.args[1] == f"{BASE_URL}/api/v1/users/123/info/"

    @pytest.mark.asyncio
    async def test_sends_body_data(self):
        """Should send body data in POST request."""
        mock_session_context, mock_session = create_mock_session(status=200)

        body_data = {"username": "testuser", "password": "testpass"}

        with patch(
            "easyinsta.utils.http.aiohttp.ClientSession",
            return_value=mock_session_context,
        ):
            await api_call("/test", method="POST", body=body_data)

        call_kwargs = mock_session.request.call_args
        assert call_kwargs.kwargs["data"] == body_data

    @pytest.mark.asyncio
    async def test_uses_provided_headers(self):
        """Should use provided headers directly."""
        mock_session_context, mock_session = create_mock_session(status=200)

        custom_headers = {"X-Custom": "value"}

        with patch(
            "easyinsta.utils.http.aiohttp.ClientSession",
            return_value=mock_session_context,
        ):
            await api_call("/test", method="GET", headers=custom_headers)

        call_kwargs = mock_session.request.call_args
        headers = call_kwargs.kwargs["headers"]

        assert headers == {"X-Custom": "value"}

    @pytest.mark.asyncio
    async def test_no_headers_provided(self):
        """Should use None when no headers provided."""
        mock_session_context, mock_session = create_mock_session(status=200)

        with patch(
            "easyinsta.utils.http.aiohttp.ClientSession",
            return_value=mock_session_context,
        ):
            await api_call("/test", method="GET")

        call_kwargs = mock_session.request.call_args
        headers = call_kwargs.kwargs["headers"]

        assert headers is None


class TestBaseUrl:
    """Tests for BASE_URL constant."""

    def test_base_url_is_instagram(self):
        """BASE_URL should be Instagram API URL."""
        assert BASE_URL == "https://i.instagram.com"
