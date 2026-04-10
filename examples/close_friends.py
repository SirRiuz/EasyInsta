"""
Example: Manage close friends list.

This example shows how to add and remove users from your close friends list.
"""

import asyncio

from easyinsta import Instagram


async def main() -> None:
    ig = Instagram()
    ig.auth.with_token("YOUR_TOKEN")

    user_id = "314216"  # zuck

    # Add user to close friends
    await ig.profiles.add_to_close_friends(user_id)
    print(f"Added user {user_id} to close friends")

    # Remove user from close friends
    await ig.profiles.remove_from_close_friends(user_id)
    print(f"Removed user {user_id} from close friends")


asyncio.run(main())
