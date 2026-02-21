"""
Custom exceptions for user-related operations.
"""


class UserNotFoundException(Exception):
    """Raised when a user is not found by ID."""

    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with id={user_id} not found")


class UserAlreadyExistsException(Exception):
    """Raised when trying to create a user with an email that already exists."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email='{email}' already exists")


class InvalidUserDataException(Exception):
    """Raised when user data validation fails."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__(f"Invalid user data: {', '.join(errors)}")


class ProfileNotFoundException(Exception):
    """Raised when a profile_id does not exist in the profiles table."""

    def __init__(self, profile_id: int):
        self.profile_id = profile_id
        super().__init__(f"Profile with id={profile_id} not found")


class InvalidVerificationToken(Exception):
    """Raised when email verification token is invalid or corrupt."""

    def __init__(self, message: str = "Invalid verification token"):
        self.message = message
        super().__init__(message)
