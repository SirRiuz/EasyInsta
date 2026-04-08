"""
Thread status constants.

This module contains the enum for thread status values.
"""

from enum import Enum


class ThreadStatus(Enum):
    """Status of a thread relative to the user."""

    NEW = "new"
    UNREAD_MARKED = "unread_marked"
    READ = "read"
