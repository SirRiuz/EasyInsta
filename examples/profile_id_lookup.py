"""
Example: Convert between username and user ID.

This example shows how to use the profile lookup methods to convert
between Instagram usernames and user IDs.
"""

import asyncio

from easyinsta import Instagram


async def main() -> None:
    ig = Instagram()
    ig.auth.with_token("YOUR_TOKEN")

    # Get user ID from username
    user_id = await ig.profiles.user_id_from_username("zuck")
    print(f"Username 'zuck' has user ID: {user_id}")

    # Get username from user ID
    username = await ig.profiles.username_from_user_id("314216")
    print(f"User ID '314216' belongs to: {username}")


asyncio.run(main())
