"""
Service layer for user business logic.
Handles validation, password hashing, and coordinates repository operations.
"""
import hashlib
import logging
from django.db import transaction, IntegrityError
from typing import Optional

from repositories import UserRepository
from dto import UserDTO, CreateUserDTO, UpdateUserDTO
from exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    InvalidUserDataException,
    ProfileNotFoundException
)

logger = logging.getLogger(__name__)


class UserService:
    """
    Business logic layer for user operations.
    """

    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, data: CreateUserDTO) -> UserDTO:
        """
        Create a new user.

        Args:
            data: User creation data

        Returns:
            Created UserDTO

        Raises:
            InvalidUserDataException: If validation fails
            UserAlreadyExistsException: If email already exists
            ProfileNotFoundException: If profile_id doesn't exist
        """
        # Validate input data
        errors = data.validate()
        if errors:
            raise InvalidUserDataException(errors)

        # Check if email already exists
        if self.repository.exists_by_email(data.email):
            raise UserAlreadyExistsException(data.email)

        # Hash password
        password_hash = self._hash_password(data.password)

        # Create user in transaction
        # Foreign key constraint will validate profile_id exists
        try:
            with transaction.atomic():
                user = self.repository.create(
                    profile_id=data.profile_id,
                    name=data.name,
                    surname=data.surname,
                    email=data.email,
                    password_hash=password_hash
                )
                return user
        except IntegrityError as e:
            # Handle database constraint violations
            error_msg = str(e).lower()
            if 'email' in error_msg and 'unique' in error_msg:
                raise UserAlreadyExistsException(data.email)
            elif 'profile_id' in error_msg or 'foreign key' in error_msg:
                raise ProfileNotFoundException(data.profile_id)
            else:
                raise

    def get_user(self, user_id: int) -> UserDTO:
        """
        Get a user by ID.

        Args:
            user_id: User ID

        Returns:
            UserDTO

        Raises:
            UserNotFoundException: If user doesn't exist
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        return user

    def get_user_by_email(self, email: str) -> Optional[UserDTO]:
        """
        Get a user by email.

        Args:
            email: User's email

        Returns:
            UserDTO if found, None otherwise
        """
        return self.repository.get_by_email(email)

    def list_users(self, limit: int = 100, offset: int = 0) -> list[UserDTO]:
        """
        Get a paginated list of users.

        Args:
            limit: Maximum number of users (max 1000)
            offset: Number of users to skip

        Returns:
            List of UserDTO objects
        """
        # Enforce maximum limit
        limit = min(limit, 1000)
        return self.repository.get_all(limit=limit, offset=offset)

    def update_user(self, user_id: int, data: UpdateUserDTO) -> UserDTO:
        """
        Update a user.

        Args:
            user_id: User ID to update
            data: Update data

        Returns:
            Updated UserDTO

        Raises:
            UserNotFoundException: If user doesn't exist
            InvalidUserDataException: If validation fails
            UserAlreadyExistsException: If email is taken by another user
        """
        # Check if there are any updates
        if not data.has_updates():
            return self.get_user(user_id)

        # Validate input data
        errors = data.validate()
        if errors:
            raise InvalidUserDataException(errors)

        # Check if user exists
        existing_user = self.repository.get_by_id(user_id)
        if not existing_user:
            raise UserNotFoundException(user_id)

        # If updating email, check if it's taken by another user
        if data.email and data.email != existing_user.email:
            user_with_email = self.repository.get_by_email(data.email)
            if user_with_email and user_with_email.id != user_id:
                raise UserAlreadyExistsException(data.email)

        # Prepare fields to update
        update_fields = {}
        if data.name is not None:
            update_fields['name'] = data.name
        if data.surname is not None:
            update_fields['surname'] = data.surname
        if data.email is not None:
            update_fields['email'] = data.email
        if data.password is not None:
            update_fields['password'] = self._hash_password(data.password)

        # Update user in transaction
        try:
            with transaction.atomic():
                updated_user = self.repository.update(user_id, **update_fields)
                return updated_user
        except IntegrityError as e:
            # Handle database constraint violations
            if 'email' in str(e).lower():
                raise UserAlreadyExistsException(data.email)
            else:
                raise

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id: User ID to delete

        Returns:
            True if deleted, False if user didn't exist
        """
        return self.repository.delete(user_id)

    def verify_password(self, user_id: int, password: str) -> bool:
        """
        Verify a user's password.
        Used for future authentication.

        Args:
            user_id: User ID
            password: Plain text password to verify

        Returns:
            True if password matches, False otherwise
        """
        stored_hash = self.repository.get_password_hash(user_id)
        if not stored_hash:
            return False

        password_hash = self._hash_password(password)
        return password_hash == stored_hash

    def _hash_password(self, password: str) -> str:
        """
        Hash a password using SHA-256.

        NOTE: For production, use bcrypt or argon2 instead.
        SHA-256 is used here for simplicity in a learning project.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def _profile_exists(self, profile_id: int) -> bool:
        """
        Check if a profile exists in the profiles table.

        Args:
            profile_id: Profile ID to check

        Returns:
            True if exists, False otherwise
        """
        from django.db import connection

        query = "SELECT COUNT(*) FROM profiles WHERE id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, (profile_id,))
            row = cursor.fetchone()
            logger.info(f"Profile check: profile_id={profile_id}, row={row}, exists={row[0] > 0 if row else False}")
            return row[0] > 0 if row else False
