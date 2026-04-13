"""
Example: Get authenticated user's account information.

This example shows how to retrieve the current user's account
information including personal details like email and phone number.
"""

import asyncio

from easyinsta import Instagram


async def main() -> None:
    ig = Instagram()

    # Authenticate with cookies
    ig.auth.with_cookies(
        sessionid="YOUR_SESSION_ID",
        ds_user_id="YOUR_USER_ID"
    )

    # Get account info
    account = await ig.account.account_info()

    # Display account information
    print(f"Username: {account.username}")
    print(f"Full Name: {account.full_name}")
    print(f"Email: {account.email}")
    print(f"Phone: {account.phone_number}")
    print(f"Biography: {account.biography}")
    print(f"Followers: {account.follower_count}")
    print(f"Following: {account.following_count}")
    print(f"Posts: {account.media_count}")
    print(f"Verified: {account.is_verified}")
    print(f"Private: {account.is_private}")


asyncio.run(main())
