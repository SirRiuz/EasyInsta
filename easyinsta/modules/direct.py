"""
Direct messages module.

This module provides functionality for interacting with Instagram direct messages.
"""

from easyinsta.models import Inbox
from easyinsta.utils.direct import fetch_inbox
from easyinsta.modules.base import AuthenticatedModule, requires_auth


class Direct(AuthenticatedModule):
    """
    Direct messages module for Instagram DMs.

    This class provides methods to retrieve and interact with
    Instagram direct message conversations.
    """

    def __init__(self, auth):
        super().__init__(auth)
        self._cursors: dict[int, str] = {}

    @requires_auth
    async def get_inbox(self, page: int = 1) -> Inbox:
        """
        Get the direct messages inbox.

        Retrieves conversation threads, paginated by 20 items.

        Note:
            This method requires authentication.
            Use thread.get_status(user_id) to check if a thread is unread.

        Args:
            page: The page number (1-indexed). Each page contains up to 20 threads.

        Returns:
            An Inbox object containing conversation threads.

        Raises:
            AuthRequiredError: If not authenticated.
            ApiError: If the API returns an error.
            ValueError: If page number is less than 1.

        Example:
            >>> ig = Instagram()
            >>> ig.auth.with_token("your_token")
            >>> inbox = await ig.direct.get_inbox(page=1)
            >>> for thread in inbox.threads:
            ...     print(thread.name)
        """
        if page < 1:
            raise ValueError("Page number must be at least 1")

        # For page 1, no cursor is needed
        current_cursor = None

        if page > 1:
            # Try to get cached cursor from previous page
            current_cursor = self._cursors.get(page - 1)

            # If cursor not cached, fetch previous pages to build cursor chain
            if current_cursor is None:
                for page_num in range(1, page):
                    # Skip if cursor already cached (except page 1 which has no cursor)
                    if page_num in self._cursors and page_num != 1:
                        continue

                    previous_cursor = self._cursors.get(page_num - 1) if page_num > 1 else None
                    response = await fetch_inbox(
                        self._get_credentials(),
                        cursor=previous_cursor,
                    )

                    # Cache cursor for next page if more results exist
                    inbox_data = response.get("inbox", {})
                    if inbox_data.get("has_older"):
                        self._cursors[page_num] = inbox_data.get("oldest_cursor", "")

                current_cursor = self._cursors.get(page - 1)

        # Fetch the requested page
        response = await fetch_inbox(self._get_credentials(), cursor=current_cursor)
        inbox = Inbox(response)

        if inbox.has_older:
            self._cursors[page] = inbox.oldest_cursor

        return inbox
