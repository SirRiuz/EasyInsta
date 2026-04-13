"""
Session management for Instagram API requests.

This module provides a file-based session storage system that persists
authentication tokens and device headers to disk (~/.easyinsta/sessions/).

When authenticating, if a session file already exists for the token, it will
be loaded instead of creating a new one. This prevents generating new device
fingerprints on every authentication, which could trigger Instagram's
security systems.

The session includes special headers that simulate requests from the official
Instagram Android app, including device identifiers, connection info, and
other metadata that Instagram uses to verify legitimate API requests.

Session files are stored as JSON with SHA256-hashed filenames for privacy.

Note:
    This session system can be disabled, but doing so will generate new device
    fingerprints on every request, making API calls more detectable by
    Instagram's bot detection systems and potentially triggering security
    challenges or account restrictions.
"""

import hashlib
import json
from pathlib import Path
from typing import Any

from easyinsta.constants import App, RequestHeaders
from easyinsta.utils import (
    generate_bandwidth_bytes,
    generate_bandwidth_speed,
    generate_bandwidth_time,
    generate_capabilities,
    generate_connection_speed,
    generate_connection_type,
    generate_device_id,
    generate_ig_did,
    generate_pigeon_rawclienttime,
    generate_pigeon_session_id,
    generate_timezone_offset,
    get_locale_for_country,
    get_random_user_agent,
)


# Default sessions directory in user's home (works on macOS and Linux)
DEFAULT_SESSIONS_DIR = Path.home() / ".easyinsta" / "sessions"


class Session:
    """
    File-based session storage for Instagram authentication.

    Persists authentication tokens and device headers to the local filesystem
    (~/.easyinsta/sessions/) to maintain consistent device fingerprints across
    requests and avoid triggering Instagram's security alerts.

    The session stores:
        - Authentication token (Bearer IGT:2:...)
        - Device headers that simulate the official Instagram Android app

    When authenticating, check if a session exists before creating a new one:
        ```python
        session = Session(token)
        if session.exists():
            session = Session.load(token)  # Reuse existing session
        else:
            session.reset_headers()  # Generate new device fingerprint
            session.save()
        ```

    Attributes:
        token: The authentication token.
        headers: Device headers that mimic the Instagram Android app.
        sessions_dir: Directory where session files are stored.
    """

    def __init__(
        self,
        token: str = "",
        headers: dict[str, str] | None = None,
        sessions_dir: Path | str | None = None,
    ):
        """
        Initialize a Session instance.

        Args:
            token: The authentication token.
            headers: Custom headers dict. If None, generates default headers.
            sessions_dir: Directory for session files. Defaults to ~/.easyinsta/sessions.
        """
        self._token = token
        self._headers = headers if headers is not None else {}
        self._sessions_dir = Path(sessions_dir) if sessions_dir else DEFAULT_SESSIONS_DIR

    @property
    def token(self) -> str:
        """Get the authentication token."""
        return self._token

    @token.setter
    def token(self, value: str) -> None:
        """Set the authentication token."""
        self._token = value

    @property
    def headers(self) -> dict[str, str]:
        """Get the session headers."""
        return self._headers.copy()

    @property
    def sessions_dir(self) -> Path:
        """Get the sessions directory path."""
        return self._sessions_dir

    @staticmethod
    def generate_default_headers(
        wifi: bool = True,
        country: str = "usa",
    ) -> dict[str, str]:
        """
        Generate headers that simulate the official Instagram Android app.

        Creates a complete set of device headers including User-Agent,
        device IDs, connection info, and other metadata that Instagram
        uses to verify legitimate API requests.

        These headers should be generated once per session and reused
        to maintain a consistent device fingerprint.

        Args:
            wifi: True for WiFi connection type, False for mobile.
            country: Country code for locale headers (e.g., "usa", "colombia").

        Returns:
            Dictionary of HTTP headers mimicking the Instagram app.
        """
        headers = {
            RequestHeaders.USER_AGENT: get_random_user_agent(),
            RequestHeaders.X_IG_APP_ID: App.ID,
            RequestHeaders.X_IG_CAPABILITIES: generate_capabilities(),
            RequestHeaders.X_IG_CONNECTION_TYPE: generate_connection_type(wifi),
            RequestHeaders.X_IG_DEVICE_ID: generate_ig_did(),
            RequestHeaders.X_IG_ANDROID_ID: generate_device_id(),
            RequestHeaders.X_IG_TIMEZONE_OFFSET: generate_timezone_offset(),
            RequestHeaders.X_IG_VALIDATE_NULL: "true",
            RequestHeaders.X_IG_BANDWIDTH_SPEED: generate_bandwidth_speed(wifi),
            RequestHeaders.X_IG_BANDWIDTH_BYTES: generate_bandwidth_bytes(),
            RequestHeaders.X_IG_BANDWIDTH_TIME: generate_bandwidth_time(),
            RequestHeaders.X_IG_WWW_CLAIM: "0",
            RequestHeaders.X_PIGEON_RAWCLIENTTIME: generate_pigeon_rawclienttime(),
            RequestHeaders.X_PIGEON_SESSION_ID: generate_pigeon_session_id(),
            RequestHeaders.X_IG_CONNECTION_SPEED: generate_connection_speed(wifi),
            RequestHeaders.X_FB_HTTP_ENGINE: "MQTT Analytics",
            RequestHeaders.X_FB_CLIENT_IP: "True",
            RequestHeaders.X_FB_SERVER_CLUSTER: "True",
            **get_locale_for_country(country),
            RequestHeaders.ACCEPT_LANGUAGE: "en-US",
            RequestHeaders.ACCEPT_ENCODING: "gzip, deflate",
        }
        return headers

    @staticmethod
    def generate_session_id(token: str) -> str:
        """
        Generate a unique session ID from a token.

        Creates a SHA256 hash of the token to use as the session filename.

        Args:
            token: The authentication token.

        Returns:
            SHA256 hash string of the token.
        """
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def generate_credentials_id(username: str, password: str) -> str:
        """
        Generate a unique ID from username and password.

        Creates a SHA256 hash of the credentials to use as the session filename.

        Args:
            username: The Instagram username.
            password: The Instagram password.

        Returns:
            SHA256 hash string of the credentials.
        """
        credentials = f"{username}:{password}"
        return hashlib.sha256(credentials.encode()).hexdigest()

    def get_session_path(self) -> Path:
        """
        Get the file path for this session.

        Returns:
            Path to the session JSON file.
        """
        session_id = self.generate_session_id(self._token)
        return self._sessions_dir / f"{session_id}.json"

    def _ensure_sessions_dir(self) -> None:
        """Create the sessions directory if it doesn't exist."""
        self._sessions_dir.mkdir(parents=True, exist_ok=True)

    def save(self) -> Path:
        """
        Save the session to a JSON file.

        Creates the sessions directory if needed and saves the token
        and headers to a JSON file named with the token's SHA256 hash.

        Returns:
            Path to the saved session file.

        Raises:
            ValueError: If no token is set.
        """
        if not self._token:
            raise ValueError("Cannot save session without a token")

        self._ensure_sessions_dir()

        session_path = self.get_session_path()
        session_data = {
            "token": self._token,
            "headers": self._headers,
        }

        with open(session_path, "w") as f:
            json.dump(session_data, f, indent=2)

        return session_path

    def save_for_credentials(self, username: str, password: str) -> Path:
        """
        Save the session to a JSON file using credentials hash as filename.

        Creates the sessions directory if needed and saves the token
        and headers to a JSON file named with the credentials SHA256 hash.

        Args:
            username: The Instagram username.
            password: The Instagram password.

        Returns:
            Path to the saved session file.

        Raises:
            ValueError: If no token is set.
        """
        if not self._token:
            raise ValueError("Cannot save session without a token")

        self._ensure_sessions_dir()

        session_id = self.generate_credentials_id(username, password)
        session_path = self._sessions_dir / f"{session_id}.json"
        session_data = {
            "token": self._token,
            "headers": self._headers,
        }

        with open(session_path, "w") as f:
            json.dump(session_data, f, indent=2)

        return session_path

    @classmethod
    def load(
        cls,
        token: str,
        sessions_dir: Path | str | None = None,
    ) -> "Session":
        """
        Load a session from a JSON file.

        Args:
            token: The authentication token (used to find the session file).
            sessions_dir: Directory where session files are stored.

        Returns:
            Session instance loaded from file.

        Raises:
            FileNotFoundError: If the session file doesn't exist.
        """
        sessions_path = Path(sessions_dir) if sessions_dir else DEFAULT_SESSIONS_DIR
        session_id = cls.generate_session_id(token)
        session_path = sessions_path / f"{session_id}.json"

        with open(session_path, "r") as f:
            session_data = json.load(f)

        return cls(
            token=session_data.get("token", ""),
            headers=session_data.get("headers", {}),
            sessions_dir=sessions_path,
        )

    @classmethod
    def load_from_path(cls, path: Path | str) -> "Session":
        """
        Load a session from a specific file path.

        Args:
            path: Path to the session JSON file.

        Returns:
            Session instance loaded from file.

        Raises:
            FileNotFoundError: If the file doesn't exist.
        """
        path = Path(path)

        with open(path, "r") as f:
            session_data = json.load(f)

        return cls(
            token=session_data.get("token", ""),
            headers=session_data.get("headers", {}),
            sessions_dir=path.parent,
        )

    def exists(self) -> bool:
        """
        Check if a session file exists for the current token.

        Returns:
            True if the session file exists, False otherwise.
        """
        if not self._token:
            return False
        return self.get_session_path().exists()

    @classmethod
    def exists_for_credentials(
        cls,
        username: str,
        password: str,
        sessions_dir: Path | str | None = None,
    ) -> bool:
        """
        Check if a session file exists for the given credentials.

        Args:
            username: The Instagram username.
            password: The Instagram password.
            sessions_dir: Directory where session files are stored.

        Returns:
            True if the session file exists, False otherwise.
        """
        sessions_path = Path(sessions_dir) if sessions_dir else DEFAULT_SESSIONS_DIR
        session_id = cls.generate_credentials_id(username, password)
        session_path = sessions_path / f"{session_id}.json"
        return session_path.exists()

    @classmethod
    def load_from_credentials(
        cls,
        username: str,
        password: str,
        sessions_dir: Path | str | None = None,
    ) -> "Session":
        """
        Load a session from credentials.

        Args:
            username: The Instagram username.
            password: The Instagram password.
            sessions_dir: Directory where session files are stored.

        Returns:
            Session instance loaded from file.

        Raises:
            FileNotFoundError: If the session file doesn't exist.
        """
        sessions_path = Path(sessions_dir) if sessions_dir else DEFAULT_SESSIONS_DIR
        session_id = cls.generate_credentials_id(username, password)
        session_path = sessions_path / f"{session_id}.json"

        with open(session_path, "r") as f:
            session_data = json.load(f)

        return cls(
            token=session_data.get("token", ""),
            headers=session_data.get("headers", {}),
            sessions_dir=sessions_path,
        )

    def delete(self) -> bool:
        """
        Delete the session file.

        Returns:
            True if the file was deleted, False if it didn't exist.
        """
        session_path = self.get_session_path()
        if session_path.exists():
            session_path.unlink()
            return True
        return False

    # Header management methods

    def set_header(self, key: str, value: str) -> None:
        """
        Set or update a single header.

        Args:
            key: Header name.
            value: Header value.
        """
        self._headers[key] = value

    def set_headers(self, headers: dict[str, str]) -> None:
        """
        Set or update multiple headers at once.

        Args:
            headers: Dictionary of headers to set/update.
        """
        self._headers.update(headers)

    def get_header(self, key: str, default: str | None = None) -> str | None:
        """
        Get a header value.

        Args:
            key: Header name.
            default: Default value if header doesn't exist.

        Returns:
            Header value or default.
        """
        return self._headers.get(key, default)

    def remove_header(self, key: str) -> bool:
        """
        Remove a header.

        Args:
            key: Header name to remove.

        Returns:
            True if the header was removed, False if it didn't exist.
        """
        if key in self._headers:
            del self._headers[key]
            return True
        return False

    def remove_headers(self, keys: list[str]) -> int:
        """
        Remove multiple headers at once.

        Args:
            keys: List of header names to remove.

        Returns:
            Number of headers that were removed.
        """
        removed = 0
        for key in keys:
            if self.remove_header(key):
                removed += 1
        return removed

    def has_header(self, key: str) -> bool:
        """
        Check if a header exists.

        Args:
            key: Header name.

        Returns:
            True if the header exists, False otherwise.
        """
        return key in self._headers

    def clear_headers(self) -> None:
        """Remove all headers."""
        self._headers.clear()

    def reset_headers(
        self,
        wifi: bool = True,
        country: str = "usa",
    ) -> None:
        """
        Reset headers to default generated values.

        Clears existing headers and generates new default headers.

        Args:
            wifi: True for WiFi connection type, False for mobile.
            country: Country code for locale headers.
        """
        self._headers = self.generate_default_headers(wifi, country)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert session to a dictionary.

        Returns:
            Dictionary with token and headers.
        """
        return {
            "token": self._token,
            "headers": self._headers.copy(),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        sessions_dir: Path | str | None = None,
    ) -> "Session":
        """
        Create a Session from a dictionary.

        Args:
            data: Dictionary with token and headers.
            sessions_dir: Directory for session files.

        Returns:
            Session instance.
        """
        return cls(
            token=data.get("token", ""),
            headers=data.get("headers", {}),
            sessions_dir=sessions_dir,
        )

    def __repr__(self) -> str:
        token_preview = f"{self._token[:8]}..." if len(self._token) > 8 else self._token
        return f"Session(token='{token_preview}', headers_count={len(self._headers)})"
