from easyinsta.utils import api_call
from easyinsta.constants import Endpoints
from easyinsta.exceptions import InvalidFormatError, MissingFieldError


class Validators:
    """
    Validation utility class for Instagram-related data.

    This class provides methods to validate various inputs such as usernames,
    emails, URLs, and other Instagram-specific data formats.

    Each validation method returns True if the input is valid.
    If the input is invalid, an appropriate exception is raised
    with a descriptive error message.
    """

    async def check_username(self, username: str) -> bool:
        """
        Validate whether an Instagram username is registered.

        Checks if the given username corresponds to an active Instagram account
        by querying the Instagram API (https://www.instagram.com/{username}/).

        Note:
            This method does not require authentication.

        Args:
            username: The Instagram username to validate (without @).

        Returns:
            True if the account exists, False otherwise.

        Raises:
            Exception: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> await ig.validators.check_username("zuck")
            True
            >>> await ig.validators.check_username("nonexistent_user_12345")
            False
        """
        data = await api_call(Endpoints.CHECK_USERNAME, body={"username": username})

        if "available" not in data:
            raise MissingFieldError("available")

        return not data["available"]

    async def check_email(self, email: str) -> bool:
        """
        Check whether an email is already registered on Instagram.

        Queries the Instagram API to determine if the given email address
        is associated with an existing account.

        Note:
            This method does not require authentication.

        Args:
            email: The email address to check.

        Returns:
            True if the email is already in use, False if it's available.

        Raises:
            InvalidFormatError: If the email format is invalid.
            MissingFieldError: If the response is missing required fields.
            Exception: If the API returns a status code other than 200.

        Example:
            >>> ig = Instagram()
            >>> await ig.validators.check_email("taken@example.com")
            True
            >>> await ig.validators.check_email("available@example.com")
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
