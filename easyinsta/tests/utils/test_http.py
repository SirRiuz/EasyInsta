"""Tests for HTTP utilities."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from easyinsta.exceptions import ApiError
from easyinsta.utils.http import BASE_URL, DEFAULT_HEADERS, api_call


def create_mock_session(status: int = 200, json_data: dict | None = None):
    """Helper to create a properly configured mock session."""
    mock_response = MagicMock()
    mock_response.status = status
    mock_response.json = AsyncMock(return_value=json_data or {})

    mock_request_context = MagicMock()
    mock_request_context.__aenter__ = AsyncMock(return_value=mock_response)
    mock_request_context.__aexit__ = AsyncMock(return_value=None)

    mock_session = MagicMock()
    mock_session.request = MagicMock(return_value=mock_request_context)

    mock_session_context = MagicMock()
    mock_session_context.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_context.__aexit__ = AsyncMock(return_value=None)

    return mock_session_context, mock_session


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

        assert result == {"user": {"id": "123"}}

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

        assert result == {"status": "ok"}

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
        """Should include default headers in request."""
        mock_session_context, mock_session = create_mock_session(status=200)

        with patch(
            "easyinsta.utils.http.aiohttp.ClientSession",
            return_value=mock_session_context,
        ):
            await api_call("/test", method="GET")

        call_kwargs = mock_session.request.call_args
        headers = call_kwargs.kwargs["headers"]

        for key, value in DEFAULT_HEADERS.items():
            assert headers[key] == value

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


class TestDefaultHeaders:
    """Tests for DEFAULT_HEADERS constant."""

    def test_contains_app_id(self):
        """Should contain X-Ig-App-Id header."""
        assert "X-Ig-App-Id" in DEFAULT_HEADERS

    def test_contains_capabilities(self):
        """Should contain X-Ig-Capabilities header."""
        assert "X-Ig-Capabilities" in DEFAULT_HEADERS

    def test_contains_connection_type(self):
        """Should contain X-Ig-Connection-Type header."""
        assert "X-Ig-Connection-Type" in DEFAULT_HEADERS

    def test_contains_accept_language(self):
        """Should contain Accept-Language header."""
        assert "Accept-Language" in DEFAULT_HEADERS

    def test_contains_content_type(self):
        """Should contain Content-Type header."""
        assert "Content-Type" in DEFAULT_HEADERS


class TestBaseUrl:
    """Tests for BASE_URL constant."""

    def test_base_url_is_instagram(self):
        """BASE_URL should be Instagram API URL."""
        assert BASE_URL == "https://i.instagram.com"
