from easyinsta.constants import Endpoints, ErrorMessages
from easyinsta.exceptions import InvalidFormatError, MissingFieldError
from easyinsta.models import Profile, ProfileLight
from easyinsta.modules.base import AuthenticatedModule, requires_auth
from easyinsta.utils import (
    api_call,
    fetch_profile_by_id,
    fetch_profile_by_id_no_auth,
    fetch_profile_by_username,
    follow_user,
    unfollow_user,
)


class Profiles(AuthenticatedModule):
    """
    Profile utility class for Instagram user profiles.

    This class provides methods to retrieve and interact with
    Instagram user profile information.
    """

    async def get_public(self, profile_id: str) -> ProfileLight:
        """
        Get public profile information by profile ID.

        Retrieves publicly available profile data without authentication.

        Note:
            This method does not require authentication.

        Args:
            profile_id: The Instagram profile ID.

        Returns:
            A ProfileLight object containing public profile information.

        Raises:
            ProfileNotFoundError: If the profile is not found.
            RateLimitError: If the API rate limit is exceeded.
            ApiError: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> profile = await ig.profiles.get_public("314216")
            >>> profile.username
            'zuck'
        """
        user_data = await fetch_profile_by_id_no_auth(profile_id)
        return ProfileLight(user_data)

    @requires_auth
    async def get(
        self,
        username: str | None = None,
        profile_id: str | None = None,
    ) -> Profile:
        """
        Get profile information by username or profile ID.

        Retrieves complete profile data. Only one parameter must be specified.

        Note:
            This method requires authentication.

        Args:
            username: The Instagram username to look up (without @).
            profile_id: The Instagram profile ID.

        Returns:
            A Profile object containing complete profile information.

        Raises:
            ValueError: If both or neither parameters are specified.
            ProfileNotFoundError: If the profile is not found.
            ApiError: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> profile = await ig.profiles.get(username="zuck")
            >>> profile.id
            '314216'
            >>> profile = await ig.profiles.get(profile_id="314216")
            >>> profile.username
            'zuck'
        """
        if username is not None and profile_id is not None:
            raise ValueError(ErrorMessages.ONLY_ONE_PARAM)

        if username is None and profile_id is None:
            raise ValueError(ErrorMessages.MISSING_PARAM)

        # NOTE: fetch_profile_by_id uses PROFILE_LIGHT endpoint which returns
        # slightly different data than PROFILE_BY_USERNAME, but Profile model
        # handles both response formats via .get() with defaults.
        fetch = fetch_profile_by_id if profile_id else fetch_profile_by_username
        user_data = await fetch(profile_id or username, self._get_credentials())

        return Profile(user_data)

    @requires_auth
    async def user_id_from_username(self, username: str) -> int:
        """
        Get user ID by username.

        Note:
            This method requires authentication.

        Args:
            username: The Instagram username (without @).

        Returns:
            The user ID as an integer.

        Raises:
            ProfileNotFoundError: If the profile is not found.
            ApiError: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> user_id = await ig.profiles.user_id_from_username("zuck")
            >>> user_id
            314216
        """
        user_data = await fetch_profile_by_username(username, self._get_credentials())
        return int(user_data["pk"])

    @requires_auth
    async def username_from_user_id(self, user_id: str) -> str:
        """
        Get username by user ID.

        Note:
            This method requires authentication.

        Args:
            user_id: The Instagram user ID.

        Returns:
            The username as a string.

        Raises:
            ProfileNotFoundError: If the profile is not found.
            ApiError: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> username = await ig.profiles.username_from_user_id("314216")
            >>> username
            'zuck'
        """
        user_data = await fetch_profile_by_id(user_id, self._get_credentials())
        return user_data["username"]

    @requires_auth
    async def follow(self, user_id: str) -> bool:
        """
        Follow a user.

        Note:
            This method requires authentication.

        Args:
            user_id: The Instagram user ID to follow.

        Returns:
            True if the follow action was successful.

        Raises:
            ApiError: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> await ig.profiles.follow("314216")
            True
        """
        await follow_user(user_id, self._get_credentials())
        return True

    @requires_auth
    async def unfollow(self, user_id: str) -> bool:
        """
        Unfollow a user.

        Note:
            This method requires authentication.

        Args:
            user_id: The Instagram user ID to unfollow.

        Returns:
            True if the unfollow action was successful.

        Raises:
            ApiError: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> await ig.profiles.unfollow("314216")
            True
        """
        await unfollow_user(user_id, self._get_credentials())
        return True

    async def exists_by_username(self, username: str) -> bool:
        """
        Check if an Instagram account exists with the given username.

        Queries the Instagram API to determine if the username is already
        registered to an existing account.

        Note:
            This method does not require authentication.

        Args:
            username: The Instagram username to check (without @).

        Returns:
            True if an account exists with this username, False if available.

        Raises:
            MissingFieldError: If the response is missing required fields.
            ApiError: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> await ig.profiles.exists_by_username("zuck")
            True
            >>> await ig.profiles.exists_by_username("nonexistent_user_12345")
            False
        """
        data = await api_call(Endpoints.CHECK_USERNAME, body={"username": username})

        if "available" not in data:
            raise MissingFieldError("available")

        return not data["available"]

    async def exists_by_email(self, email: str) -> bool:
        """
        Check if an Instagram account exists with the given email.

        Queries the Instagram API to determine if the email address is already
        registered to an existing account.

        Note:
            This method does not require authentication.

        Args:
            email: The email address to check.

        Returns:
            True if an account exists with this email, False if available.

        Raises:
            InvalidFormatError: If the email format is invalid.
            MissingFieldError: If the response is missing required fields.
            ApiError: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> await ig.profiles.exists_by_email("taken@example.com")
            True
            >>> await ig.profiles.exists_by_email("available@example.com")
            False
        """
        data = await api_call(Endpoints.CHECK_EMAIL, body={"email": email})

        if "valid" not in data:
            raise MissingFieldError("valid")

        if not data["valid"]:
            raise InvalidFormatError("email")

        if "available" not in data:
            raise MissingFieldError("available")

        return not data["available"]
