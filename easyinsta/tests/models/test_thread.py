"""Tests for Thread model."""

import pytest

from easyinsta.constants import ThreadStatus
from easyinsta.models.thread import Thread


class TestThread:
    """Tests for Thread model."""

    def test_initializes_with_data(self):
        """Should initialize with thread data."""
        data = {
            "thread_id": "12345",
            "thread_title": "Test Thread",
            "last_activity_at": 1234567890,
            "marked_as_unread": True,
            "users": [{"username": "testuser", "full_name": "Test User"}],
        }

        thread = Thread(data)

        assert thread.thread_id == "12345"
        assert thread.thread_title == "Test Thread"
        assert thread.last_activity_at == 1234567890
        assert thread.marked_as_unread is True
        assert len(thread.users) == 1

    def test_handles_missing_fields(self):
        """Should handle missing fields with defaults."""
        thread = Thread({})

        assert thread.thread_id == ""
        assert thread.thread_title == ""
        assert thread.last_activity_at == 0
        assert thread.marked_as_unread is False
        assert thread.users == []

    def test_name_returns_thread_title(self):
        """Should return thread_title as name when available."""
        data = {
            "thread_title": "Group Chat",
            "users": [{"username": "user1", "full_name": "User One"}],
        }

        thread = Thread(data)

        assert thread.name == "Group Chat"

    def test_name_returns_full_name_when_no_title(self):
        """Should return first user's full_name when no thread_title."""
        data = {
            "thread_title": "",
            "users": [{"username": "user1", "full_name": "User One"}],
        }

        thread = Thread(data)

        assert thread.name == "User One"

    def test_name_returns_username_when_no_title_or_full_name(self):
        """Should return username when no thread_title or full_name."""
        data = {
            "thread_title": "",
            "users": [{"username": "user1"}],
        }

        thread = Thread(data)

        assert thread.name == "user1"

    def test_name_returns_unknown_when_no_users(self):
        """Should return 'Unknown Chat' when no users."""
        thread = Thread({"users": []})

        assert thread.name == "Unknown Chat"

    def test_username_returns_first_user(self):
        """Should return first user's username with @."""
        data = {
            "users": [{"username": "testuser"}],
        }

        thread = Thread(data)

        assert thread.username == "@testuser"

    def test_username_returns_unknown_when_no_users(self):
        """Should return '@unknown' when no users."""
        thread = Thread({"users": []})

        assert thread.username == "@unknown"

    def test_username_handles_missing_username(self):
        """Should handle user without username field."""
        data = {"users": [{"full_name": "Test User"}]}

        thread = Thread(data)

        assert thread.username == "@unknown"

    def test_raw_property(self):
        """Should provide access to raw data."""
        data = {"thread_id": "123", "custom_field": "value"}

        thread = Thread(data)

        assert thread.raw == data
        assert thread.raw["custom_field"] == "value"

    def test_repr(self):
        """Should have informative repr."""
        data = {"thread_id": "123", "thread_title": "Test Chat", "users": []}

        thread = Thread(data)

        assert repr(thread) == "Thread(id='123', name='Test Chat')"

    def test_last_seen_at_initialization(self):
        """Should initialize last_seen_at from data."""
        data = {
            "last_seen_at": {"123": {"timestamp": "1000"}},
        }

        thread = Thread(data)

        assert thread.last_seen_at == {"123": {"timestamp": "1000"}}


class TestThreadGetStatus:
    """Tests for Thread.get_status method."""

    def test_returns_new_when_never_seen(self):
        """Should return NEW when user has never seen the thread."""
        data = {
            "last_activity_at": 1234567890,
            "last_seen_at": {},
            "marked_as_unread": False,
        }

        thread = Thread(data)

        assert thread.get_status("user123") == ThreadStatus.NEW

    def test_returns_new_when_activity_after_last_seen(self):
        """Should return NEW when there's activity after last seen."""
        data = {
            "last_activity_at": 2000,
            "last_seen_at": {"user123": {"timestamp": "1000"}},
            "marked_as_unread": False,
        }

        thread = Thread(data)

        assert thread.get_status("user123") == ThreadStatus.NEW

    def test_returns_unread_marked_when_seen_but_marked(self):
        """Should return UNREAD_MARKED when seen but manually marked."""
        data = {
            "last_activity_at": 1000,
            "last_seen_at": {"user123": {"timestamp": "2000"}},
            "marked_as_unread": True,
        }

        thread = Thread(data)

        assert thread.get_status("user123") == ThreadStatus.UNREAD_MARKED

    def test_returns_read_when_seen_and_no_new_activity(self):
        """Should return READ when seen and no new activity."""
        data = {
            "last_activity_at": 1000,
            "last_seen_at": {"user123": {"timestamp": "2000"}},
            "marked_as_unread": False,
        }

        thread = Thread(data)

        assert thread.get_status("user123") == ThreadStatus.READ

    def test_returns_read_on_invalid_timestamp(self):
        """Should return READ when timestamps are invalid."""
        data = {
            "last_activity_at": "invalid",
            "last_seen_at": {"user123": {"timestamp": "also_invalid"}},
            "marked_as_unread": False,
        }

        thread = Thread(data)

        assert thread.get_status("user123") == ThreadStatus.READ

    def test_returns_new_for_different_user(self):
        """Should return NEW for a user not in last_seen_at."""
        data = {
            "last_activity_at": 1000,
            "last_seen_at": {"other_user": {"timestamp": "2000"}},
            "marked_as_unread": False,
        }

        thread = Thread(data)

        assert thread.get_status("user123") == ThreadStatus.NEW


class TestThreadIsUnread:
    """Tests for Thread.is_unread method."""

    def test_returns_true_for_new(self):
        """Should return True for NEW status."""
        data = {
            "last_activity_at": 2000,
            "last_seen_at": {"user123": {"timestamp": "1000"}},
        }

        thread = Thread(data)

        assert thread.is_unread("user123") is True

    def test_returns_true_for_unread_marked(self):
        """Should return True for UNREAD_MARKED status."""
        data = {
            "last_activity_at": 1000,
            "last_seen_at": {"user123": {"timestamp": "2000"}},
            "marked_as_unread": True,
        }

        thread = Thread(data)

        assert thread.is_unread("user123") is True

    def test_returns_false_for_read(self):
        """Should return False for READ status."""
        data = {
            "last_activity_at": 1000,
            "last_seen_at": {"user123": {"timestamp": "2000"}},
            "marked_as_unread": False,
        }

        thread = Thread(data)

        assert thread.is_unread("user123") is False
