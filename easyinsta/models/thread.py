"""
Thread data model.

This module contains the data model for direct message threads.
"""

from easyinsta.constants import ThreadStatus
from easyinsta.models.base import BaseModel


class Thread(BaseModel):
    """
    Direct message thread data model.

    Represents a conversation thread from the Instagram inbox.

    Attributes:
        thread_id (str): The unique thread identifier.
        thread_title (str): The thread title or name.
        last_activity_at (int): Timestamp of last activity.
        marked_as_unread (bool): Whether the thread is marked as unread.
        last_seen_at (dict): Dictionary of user_id -> last seen timestamp.
        users (list): List of users in the thread.
        raw (dict): The complete raw API response data.
    """

    def __init__(self, data: dict):
        """
        Initialize a Thread instance.

        Args:
            data: The raw API response data.
        """
        super().__init__(data)
        self.thread_id: str = data.get("thread_id", "")
        self.thread_title: str = data.get("thread_title", "")
        self.last_activity_at: int = data.get("last_activity_at", 0)
        self.marked_as_unread: bool = data.get("marked_as_unread", False)
        self.last_seen_at: dict = data.get("last_seen_at", {})
        self.users: list = data.get("users", [])

    @property
    def name(self) -> str:
        """
        Get the display name for this thread.

        Returns the thread title if available, otherwise uses the first user's
        full name or username.

        Returns:
            The display name for the thread.
        """
        if self.thread_title:
            return self.thread_title

        if self.users:
            user = self.users[0]
            return user.get("full_name") or user.get("username", "Unknown")

        return "Unknown Chat"

    @property
    def username(self) -> str:
        """
        Get the username of the first user in the thread.

        Returns:
            The username prefixed with @, or @unknown if not available.
        """
        if self.users:
            return f"@{self.users[0].get('username', 'unknown')}"
        return "@unknown"

    def get_status(self, user_id: str) -> ThreadStatus:
        """
        Get the status of this thread for a specific user.

        Determines if the thread has new messages, is marked as unread,
        or has been read.

        Args:
            user_id: The Instagram user ID to check status for.

        Returns:
            ThreadStatus.NEW: Never seen or has new activity since last seen.
            ThreadStatus.UNREAD_MARKED: Already seen but manually marked as unread.
            ThreadStatus.READ: Already seen and no new activity.
        """
        my_seen = self.last_seen_at.get(user_id)

        # Never seen this thread
        if not my_seen:
            return ThreadStatus.NEW

        try:
            last_seen_timestamp = int(my_seen.get("timestamp", 0))
            last_activity = int(self.last_activity_at)
        except (TypeError, ValueError):
            return ThreadStatus.READ

        # New activity since last seen
        if last_activity > last_seen_timestamp:
            return ThreadStatus.NEW

        # Seen but manually marked as unread
        if self.marked_as_unread:
            return ThreadStatus.UNREAD_MARKED

        return ThreadStatus.READ

    def is_unread(self, user_id: str) -> bool:
        """
        Check if this thread has unread content for a specific user.

        Args:
            user_id: The Instagram user ID to check.

        Returns:
            True if the thread is NEW or UNREAD_MARKED, False otherwise.
        """
        status = self.get_status(user_id)
        return status in (ThreadStatus.NEW, ThreadStatus.UNREAD_MARKED)

    def __repr__(self) -> str:
        return f"Thread(id='{self.thread_id}', name='{self.name}')"
