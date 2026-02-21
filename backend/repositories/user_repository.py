"""
Repository for user data access operations.
All database interactions for the users table.
"""
from typing import Optional
from .base_repository import BaseRepository
from dto import UserDTO
from exceptions import UserNotFoundException


class UserRepository(BaseRepository):
    """
    Data access layer for users table.
    Uses raw SQL queries (no ORM).
    """

    def create(
        self,
        profile_id: Optional[int],
        name: str,
        surname: str,
        email: str,
        password_hash: str,
        is_verified: bool = False,
    ) -> UserDTO:
        """
        Insert a new user into the database.

        Args:
            profile_id: Foreign key to profiles table (nullable)
            name: User's first name
            surname: User's last name
            email: User's email (must be unique)
            password_hash: Hashed password (NOT plain text)
            is_verified: Whether the user has verified their email

        Returns:
            UserDTO with the created user data

        Raises:
            IntegrityError: If email is not unique or profile_id doesn't exist
        """
        query = """
            INSERT INTO users (profile_id, name, surname, email, password, is_verified)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, profile_id, name, surname, email, is_verified
        """
        row = self.execute_one(
            query, (profile_id, name, surname, email, password_hash, is_verified)
        )
        return self._row_to_dto(row)

    def get_by_id(self, user_id: int) -> Optional[UserDTO]:
        """
        Get a user by ID.

        Args:
            user_id: User ID

        Returns:
            UserDTO if found, None otherwise
        """
        query = """
            SELECT id, profile_id, name, surname, email, is_verified
            FROM users
            WHERE id = %s
        """
        row = self.execute_one(query, (user_id,))
        return self._row_to_dto(row) if row else None

    def get_by_email(self, email: str) -> Optional[UserDTO]:
        """
        Get a user by email.

        Args:
            email: User's email

        Returns:
            UserDTO if found, None otherwise
        """
        query = """
            SELECT id, profile_id, name, surname, email, is_verified
            FROM users
            WHERE email = %s
        """
        row = self.execute_one(query, (email,))
        return self._row_to_dto(row) if row else None

    def get_all(self, limit: int = 100, offset: int = 0) -> list[UserDTO]:
        """
        Get all users with pagination.

        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip

        Returns:
            List of UserDTO objects
        """
        query = """
            SELECT id, profile_id, name, surname, email, is_verified
            FROM users
            ORDER BY id
            LIMIT %s OFFSET %s
        """
        rows = self.execute_query(query, (limit, offset))
        return [self._row_to_dto(row) for row in rows]

    def update(self, user_id: int, **fields) -> UserDTO:
        """
        Update user fields dynamically.

        Args:
            user_id: User ID to update
            **fields: Fields to update (name, surname, email, password)

        Returns:
            Updated UserDTO

        Raises:
            UserNotFoundException: If user doesn't exist
        """
        if not fields:
            # No fields to update, just return current data
            user = self.get_by_id(user_id)
            if not user:
                raise UserNotFoundException(user_id)
            return user

        # Build dynamic UPDATE query
        set_clauses = []
        params = []

        for field, value in fields.items():
            set_clauses.append(f"{field} = %s")
            params.append(value)

        params.append(user_id)

        query = f"""
            UPDATE users
            SET {', '.join(set_clauses)}
            WHERE id = %s
            RETURNING id, profile_id, name, surname, email, is_verified
        """

        row = self.execute_one(query, tuple(params))
        if not row:
            raise UserNotFoundException(user_id)

        return self._row_to_dto(row)

    def delete(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        Args:
            user_id: User ID to delete

        Returns:
            True if deleted, False if user didn't exist
        """
        query = "DELETE FROM users WHERE id = %s"
        rows_affected = self.execute_update(query, (user_id,))
        return rows_affected > 0

    def exists_by_email(self, email: str) -> bool:
        """
        Check if a user with the given email exists.

        Args:
            email: Email to check

        Returns:
            True if exists, False otherwise
        """
        query = "SELECT EXISTS(SELECT 1 FROM users WHERE email = %s)"
        row = self.execute_one(query, (email,))
        return row[0] if row else False

    def get_password_hash(self, user_id: int) -> Optional[str]:
        """
        Get the password hash for a user.
        Used for authentication - password is not included in UserDTO for security.

        Args:
            user_id: User ID

        Returns:
            Password hash if found, None otherwise
        """
        query = "SELECT password FROM users WHERE id = %s"
        row = self.execute_one(query, (user_id,))
        return row[0] if row else None

    @staticmethod
    def _row_to_dto(row: tuple) -> UserDTO:
        """
        Convert a database row to UserDTO.

        Args:
            row: Tuple of (id, profile_id, name, surname, email, is_verified)

        Returns:
            UserDTO object
        """
        return UserDTO(
            id=row[0],
            profile_id=row[1],
            name=row[2],
            surname=row[3],
            email=row[4],
            is_verified=row[5] if len(row) > 5 else False,
        )
