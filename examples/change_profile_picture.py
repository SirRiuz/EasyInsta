"""
Example: Change and remove profile picture.

This example shows how to change and remove the authenticated user's profile picture.
"""

import asyncio
from io import BytesIO

from easyinsta import Instagram


async def main() -> None:
    ig = Instagram()

    # Authenticate with cookies
    ig.auth.with_cookies(
        sessionid="YOUR_SESSION_ID",
        ds_user_id="YOUR_USER_ID"
    )

    # Option 1: Change profile picture using a local file
    with open("photo.jpg", "rb") as f:
        image = BytesIO(f.read())

    await ig.account.change_profile_picture(image=image)
    print("Profile picture changed successfully (from file)!")

    # Option 2: Change profile picture using a URL
    await ig.account.change_profile_picture(
        url="https://example.com/photo.jpg"
    )
    print("Profile picture changed successfully (from URL)!")

    # Remove profile picture (reset to default avatar)
    await ig.account.remove_profile_picture()
    print("Profile picture removed successfully!")


asyncio.run(main())
