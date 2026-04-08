from easyinsta.constants import ErrorMessages
from easyinsta.models import Profile, ProfileLight
from easyinsta.modules.base import AuthenticatedModule, requires_auth
from easyinsta.utils import (
    fetch_profile_by_id,
    fetch_profile_by_id_no_auth,
    fetch_profile_by_username,
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
