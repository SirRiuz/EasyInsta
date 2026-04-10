"""
Example: Block and unblock users.

This example shows how to block and unblock Instagram users.
"""

import asyncio

from easyinsta import Instagram


async def main() -> None:
    ig = Instagram()
    ig.auth.with_token("YOUR_TOKEN")

    user_id = "314216"  # zuck

    # Block user
    await ig.profiles.block(user_id)
    print(f"Blocked user {user_id}")

    # Unblock user
    await ig.profiles.unblock(user_id)
    print(f"Unblocked user {user_id}")


asyncio.run(main())
