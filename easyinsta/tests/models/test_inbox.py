"""Tests for Inbox model."""

import pytest

from easyinsta.models.inbox import Inbox
from easyinsta.models.thread import Thread


class TestInbox:
    """Tests for Inbox model."""

    def test_initializes_with_data(self):
        """Should initialize with inbox data."""
        data = {
            "inbox": {
                "threads": [
                    {"thread_id": "1", "users": []},
                    {"thread_id": "2", "users": []},
                ],
                "has_older": True,
                "oldest_cursor": "abc123",
            }
        }

        inbox = Inbox(data)

        assert len(inbox.threads) == 2
        assert inbox.has_older is True
        assert inbox.oldest_cursor == "abc123"

    def test_threads_are_thread_instances(self):
        """Should convert threads to Thread instances."""
        data = {
            "inbox": {
                "threads": [
                    {"thread_id": "1", "thread_title": "Chat 1", "users": []},
                ],
                "has_older": False,
                "oldest_cursor": "",
            }
        }

        inbox = Inbox(data)

        assert isinstance(inbox.threads[0], Thread)
        assert inbox.threads[0].thread_id == "1"
        assert inbox.threads[0].thread_title == "Chat 1"

    def test_handles_empty_inbox(self):
        """Should handle empty inbox data."""
        data = {"inbox": {}}

        inbox = Inbox(data)

        assert inbox.threads == []
        assert inbox.has_older is False
        assert inbox.oldest_cursor == ""

    def test_handles_missing_inbox_key(self):
        """Should handle missing inbox key."""
        inbox = Inbox({})

        assert inbox.threads == []
        assert inbox.has_older is False
        assert inbox.oldest_cursor == ""

    def test_raw_property(self):
        """Should provide access to raw data."""
        data = {
            "inbox": {"threads": [], "has_older": False},
            "extra_field": "value",
        }

        inbox = Inbox(data)

        assert inbox.raw == data
        assert inbox.raw["extra_field"] == "value"

    def test_repr(self):
        """Should have informative repr."""
        data = {
            "inbox": {
                "threads": [{"thread_id": "1", "users": []}],
                "has_older": True,
                "oldest_cursor": "cursor",
            }
        }

        inbox = Inbox(data)

        assert repr(inbox) == "Inbox(threads=1, has_older=True)"
