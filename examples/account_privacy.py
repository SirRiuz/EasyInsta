"""
Example: Set account privacy (public/private).

This example shows how to change the account privacy settings
between public and private.
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

    # Set account to public
    await ig.account.set_public()
    print("Account is now public")

    # Set account to private
    await ig.account.set_private()
    print("Account is now private")


asyncio.run(main())
