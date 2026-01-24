"""
Data Transfer Objects for user operations.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserDTO:
    """
    Full user data representation (read from database).
    Does NOT include password hash for security.
    """
    id: int
    profile_id: Optional[int]
    name: str
    surname: str
    email: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email
        }


@dataclass
class CreateUserDTO:
    """
    Data required to create a new user.
    Password is in plain text (will be hashed by service layer).
    profile_id is optional - user can fill profile later.
    """
    name: str
    surname: str
    email: str
    password: str
    profile_id: Optional[int] = None

    def validate(self) -> list[str]:
        """
        Validate user data.
        Returns list of error messages (empty if valid).
        """
        errors = []

        if not self.name or not self.name.strip():
            errors.append("Name cannot be empty")

        if not self.surname or not self.surname.strip():
            errors.append("Surname cannot be empty")

        if not self.email or '@' not in self.email:
            errors.append("Email must be valid and contain '@'")

        if not self.password or len(self.password) < 8:
            errors.append("Password must be at least 8 characters long")

        if self.profile_id is not None and self.profile_id <= 0:
            errors.append("Profile ID must be a positive integer")

        return errors


@dataclass
class UpdateUserDTO:
    """
    Data for updating an existing user.
    All fields are optional - only provided fields will be updated.
    """
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    def validate(self) -> list[str]:
        """
        Validate only the provided fields.
        Returns list of error messages (empty if valid).
        """
        errors = []

        if self.name is not None and (not self.name or not self.name.strip()):
            errors.append("Name cannot be empty")

        if self.surname is not None and (not self.surname or not self.surname.strip()):
            errors.append("Surname cannot be empty")

        if self.email is not None and (not self.email or '@' not in self.email):
            errors.append("Email must be valid and contain '@'")

        if self.password is not None and len(self.password) < 8:
            errors.append("Password must be at least 8 characters long")

        return errors

    def has_updates(self) -> bool:
        """Check if there are any fields to update."""
        return any([
            self.name is not None,
            self.surname is not None,
            self.email is not None,
            self.password is not None
        ])
