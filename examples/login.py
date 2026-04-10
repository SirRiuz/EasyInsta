"""
Example: Login with username and password.

This example shows how to authenticate using your Instagram
username and password.
"""

import asyncio

from easyinsta import Instagram
from easyinsta.exceptions import AuthenticationError


async def main() -> None:
    ig = Instagram()

    try:
        await ig.auth.login("YOUR_USERNAME", "YOUR_PASSWORD")
        print(f"Authenticated: {ig.auth.is_authenticated}")

        # Now you can use authenticated methods
        profile = await ig.profiles.get(username="zuck")
        print(f"Profile: {profile.username}")

    except AuthenticationError as e:
        print(f"Login failed: {e.message}")


asyncio.run(main())
