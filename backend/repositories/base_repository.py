"""
Base repository class with common database operations.
All queries use parameterized statements for SQL injection protection.
"""
from contextlib import contextmanager
from django.db import connection
from typing import Any, Optional


class BaseRepository:
    """
    Base class for all repositories.
    Provides common database operations using raw SQL.
    """

    @contextmanager
    def get_cursor(self):
        """
        Context manager for getting a database cursor.

        Usage:
            with self.get_cursor() as cursor:
                cursor.execute(...)
        """
        with connection.cursor() as cursor:
            yield cursor

    def execute_query(self, query: str, params: Optional[tuple] = None) -> list[tuple]:
        """
        Execute a SELECT query and return all rows.

        Args:
            query: SQL SELECT statement
            params: Query parameters (for parameterized queries)

        Returns:
            List of rows as tuples
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def execute_one(self, query: str, params: Optional[tuple] = None) -> Optional[tuple]:
        """
        Execute a SELECT query and return one row.

        Args:
            query: SQL SELECT statement
            params: Query parameters (for parameterized queries)

        Returns:
            Single row as tuple or None if not found
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

    def execute_insert(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Execute an INSERT statement with RETURNING id.

        Args:
            query: SQL INSERT statement with RETURNING id
            params: Query parameters

        Returns:
            ID of the inserted row
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result[0] if result else None

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Execute an UPDATE or DELETE statement.

        Args:
            query: SQL UPDATE or DELETE statement
            params: Query parameters

        Returns:
            Number of affected rows
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.rowcount
