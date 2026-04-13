"""
Account module.

This module provides methods for retrieving the authenticated user's account information.
"""

from io import BytesIO

from easyinsta.constants import Endpoints, RequestHeaders
from easyinsta.models.account import Account as AccountModel
from easyinsta.modules.base import AuthenticatedModule, requires_auth
from easyinsta.utils import api_call, download_image, upload_photo


class Account(AuthenticatedModule):
    """
    Account module for the authenticated user.

    Provides methods to retrieve and manage the authenticated user's account.
    """

    @requires_auth
    async def account_info(self) -> AccountModel:
        """
        Get the authenticated user's account information.

        Retrieves complete account data for the currently authenticated user,
        including personal information like email, phone number, and birthday
        that is only available for the authenticated user's own account.

        Note:
            This method requires authentication.

        Returns:
            An Account object containing the user's account information.

        Raises:
            AuthRequiredError: If not authenticated.
            ApiError: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> await ig.auth.login("username", "password")
            >>> account = await ig.account.account_info()
            >>> account.username
            'my_username'
            >>> account.email
            'my_email@example.com'
        """
        data = await api_call(
            Endpoints.CURRENT_USER,
            method="GET",
            headers=self._get_credentials(),
        )
        return AccountModel(data.get("user", {}))

    @requires_auth
    async def set_public(self) -> bool:
        """
        Set the authenticated user's account to public.

        Makes the account visible to everyone.

        Note:
            This method requires authentication.

        Returns:
            True if the account was successfully set to public.

        Raises:
            AuthRequiredError: If not authenticated.
            ApiError: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> await ig.auth.login("username", "password")
            >>> await ig.account.set_public()
            True
        """
        await api_call(
            Endpoints.SET_PUBLIC,
            method="POST",
            headers=self._get_credentials(),
        )
        return True

    @requires_auth
    async def set_private(self) -> bool:
        """
        Set the authenticated user's account to private.

        Makes the account visible only to approved followers.

        Note:
            This method requires authentication.

        Returns:
            True if the account was successfully set to private.

        Raises:
            AuthRequiredError: If not authenticated.
            ApiError: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> await ig.auth.login("username", "password")
            >>> await ig.account.set_private()
            True
        """
        await api_call(
            Endpoints.SET_PRIVATE,
            method="POST",
            headers=self._get_credentials(),
        )
        return True

    @requires_auth
    async def change_profile_picture(
        self,
        image: BytesIO | None = None,
        url: str | None = None,
    ) -> bool:
        """
        Change the authenticated user's profile picture.

        Uploads a new profile picture for the authenticated user. You can provide
        either a BytesIO object with image bytes or a URL to download the image from.

        Note:
            This method requires authentication.
            You must provide either `image` or `url`, but not both.

        Args:
            image: A BytesIO object containing the image bytes (JPEG recommended).
            url: A URL to download the image from.

        Returns:
            True if the profile picture was successfully changed.

        Raises:
            ValueError: If both image and url are provided, or neither is provided.
            AuthRequiredError: If not authenticated.
            ApiError: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> await ig.auth.login("username", "password")
            >>>
            >>> # Using BytesIO
            >>> with open("photo.jpg", "rb") as f:
            ...     image = BytesIO(f.read())
            >>> await ig.account.change_profile_picture(image=image)
            True
            >>>
            >>> # Using URL
            >>> await ig.account.change_profile_picture(url="https://example.com/photo.jpg")
            True
        """
        if image is not None and url is not None:
            raise ValueError("Cannot provide both 'image' and 'url'. Choose one.")

        if image is None and url is None:
            raise ValueError("Must provide either 'image' or 'url'.")

        if url is not None:
            image = await download_image(url)

        upload_id = upload_photo(image, self._get_credentials())

        if upload_id is None:
            raise RuntimeError("Failed to upload image")

        # # Step 2: Change profile picture using the upload_id
        # device_id = self.auth.session.get_header(RequestHeaders.X_IG_DEVICE_ID)

        headers=self._get_credentials()

        body = {
            "upload_id": upload_id,
            "use_fbuploader": "true",
            "remove_birthday_selfie": "False",
            "_uuid": headers["X-Ig-Device-Id"],
        }

        await api_call(
            Endpoints.CHANGE_PROFILE_PICTURE,
            method="POST",
            headers=headers,
            body=body,
        )

        return True

    @requires_auth
    async def remove_profile_picture(self) -> bool:
        """
        Remove the authenticated user's profile picture.

        Removes the current profile picture and resets it to the default avatar.

        Note:
            This method requires authentication.

        Returns:
            True if the profile picture was successfully removed.

        Raises:
            AuthRequiredError: If not authenticated.
            ApiError: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> await ig.auth.login("username", "password")
            >>> await ig.account.remove_profile_picture()
            True
        """
        await api_call(
            Endpoints.REMOVE_PROFILE_PICTURE,
            method="POST",
            headers=self._get_credentials(),
        )
        return True
