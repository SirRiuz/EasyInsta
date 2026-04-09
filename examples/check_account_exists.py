"""
Example: Check if an Instagram account exists.

This example shows how to check if an Instagram account exists
by username or email without requiring authentication.
"""

import asyncio

from easyinsta import Instagram


async def main() -> None:
    ig = Instagram()

    # Check if account exists by username (no auth required)
    exists = await ig.profiles.exists_by_username("zuck")
    print(f"Account 'zuck' exists: {exists}")

    exists = await ig.profiles.exists_by_username("nonexistent_user_12345")
    print(f"Account 'nonexistent_user_12345' exists: {exists}")

    # Check if account exists by email (no auth required)
    exists = await ig.profiles.exists_by_email("test@example.com")
    print(f"Account with 'test@example.com' exists: {exists}")


asyncio.run(main())
