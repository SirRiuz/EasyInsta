"""
Inbox data model.

This module contains the data model for the direct messages inbox.
"""

from easyinsta.models.base import BaseModel
from easyinsta.models.thread import Thread


class Inbox(BaseModel):
    """
    Inbox data model.

    Represents the direct messages inbox with pagination support.

    Attributes:
        threads (list[Thread]): List of conversation threads.
        has_older (bool): Whether there are older threads to fetch.
        oldest_cursor (str): Cursor for pagination to fetch older threads.
        raw (dict): The complete raw API response data.
    """

    def __init__(self, data: dict):
        """
        Initialize an Inbox instance.

        Args:
            data: The raw API response data.
        """
        super().__init__(data)
        inbox_data = data.get("inbox", {})
        self.threads: list[Thread] = [
            Thread(thread) for thread in inbox_data.get("threads", [])
        ]
        self.has_older: bool = inbox_data.get("has_older", False)
        self.oldest_cursor: str = inbox_data.get("oldest_cursor", "")

    def __repr__(self) -> str:
        return f"Inbox(threads={len(self.threads)}, has_older={self.has_older})"
