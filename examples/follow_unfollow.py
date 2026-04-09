"""
Example: Follow and unfollow users.

This example shows how to follow and unfollow Instagram users by their user ID.
"""

import asyncio

from easyinsta import Instagram


async def main() -> None:
    ig = Instagram()
    ig.auth.with_token("YOUR_TOKEN")

    user_id = "314216"  # zuck

    # Follow user
    await ig.profiles.follow(user_id)
    print(f"Followed user {user_id}")

    # Unfollow user
    await ig.profiles.unfollow(user_id)
    print(f"Unfollowed user {user_id}")


asyncio.run(main())
