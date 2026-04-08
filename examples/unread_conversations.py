"""
Example: View unread and marked-as-unread conversations.

This example shows how to fetch inbox conversations and filter them
by their read status using ThreadStatus.
"""

import asyncio

from easyinsta import Instagram
from easyinsta.constants import ThreadStatus


MY_USER_ID = "YOUR_USER_ID"


async def main() -> None:
    ig = Instagram()
    ig.auth.with_token("YOUR_TOKEN")

    inbox = await ig.direct.get_inbox(page=1)

    print("\n=== Unread Conversations ===\n")

    for thread in inbox.threads:
        status = thread.get_status(MY_USER_ID)

        # Skip already read conversations
        if status == ThreadStatus.READ:
            continue

        if status == ThreadStatus.NEW:
            print(f"🟢 [NEW] {thread.name} ({thread.username})")
        elif status == ThreadStatus.UNREAD_MARKED:
            print(f"🟡 [MARKED] {thread.name} ({thread.username})")

    # Pagination example
    if inbox.has_older:
        print(f"\n... {inbox.oldest_cursor} more conversations available")


asyncio.run(main())
