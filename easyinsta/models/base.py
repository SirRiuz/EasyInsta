"""
Base model class.

This module contains the abstract base class for all data models.
"""

from abc import ABC


class BaseModel(ABC):
    """
    Abstract base class for all data models.

    Provides common functionality for storing and accessing raw API response data.

    Attributes:
        raw (dict): The complete raw API response data.
    """

    def __init__(self, data: dict):
        """
        Initialize a BaseModel instance.

        Args:
            data: The raw API response data.
        """
        self.__data = data

    @property
    def raw(self) -> dict:
        """
        Get the complete raw API response data.

        Returns:
            The complete raw JSON response as a dictionary.
        """
        return self.__data
