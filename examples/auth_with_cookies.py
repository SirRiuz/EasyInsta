"""
Example: Authenticate with cookies.

This example shows how to authenticate using Instagram cookies
(sessionid and ds_user_id) instead of a pre-generated token.
"""

import asyncio

from easyinsta import Instagram


async def main() -> None:
    ig = Instagram()

    # Authenticate using cookies from browser
    # 1. Log in to Instagram in your browser (instagram.com)
    # 2. Open Developer Tools (F12 or Ctrl+Shift+I)
    # 3. Go to Application tab > Cookies > instagram.com
    # 4. Find and copy the values of "sessionid" and "ds_user_id" cookies
    ig.auth.with_cookies(
        sessionid="YOUR_SESSION_ID",
        ds_user_id="YOUR_USER_ID"
    )

    print(f"Authenticated: {ig.auth.is_authenticated}")

    # Now you can use authenticated methods
    profile = await ig.profiles.get(username="zuck")
    print(f"Profile: {profile.username}")


asyncio.run(main())
