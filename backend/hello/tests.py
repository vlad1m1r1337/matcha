from django.db import connection
from django.test import TransactionTestCase


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS profiles (
  id SERIAL PRIMARY KEY,
  sex TEXT NOT NULL CHECK (sex IN ('male', 'female', 'other')),
  sexual_preferences TEXT NOT NULL CHECK (sexual_preferences IN ('male', 'female', 'both', 'other')),
  biography TEXT,
  list_of_interests TEXT[] NOT NULL DEFAULT '{}',
  fame INTEGER NOT NULL DEFAULT 0 CHECK (fame >= 0),
  longitude NUMERIC(9,6),
  latitude  NUMERIC(9,6)
);

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  profile_id INTEGER NOT NULL UNIQUE REFERENCES profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS images (
  id SERIAL PRIMARY KEY,
  profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  is_avatar BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE UNIQUE INDEX IF NOT EXISTS images_one_avatar_per_profile
  ON images (profile_id)
  WHERE is_avatar = TRUE;
"""


TEARDOWN_SQL = """
DROP TABLE IF EXISTS images CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS profiles CASCADE;
"""


class RawSqlCrudTests(TransactionTestCase):
    """
    CRUD tests using bare SQL (no Django ORM models).

    These tests create the schema inside Django's test database and then
    exercise INSERT/SELECT/UPDATE/DELETE via `connection.cursor()`.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.cursor() as cursor:
            cursor.execute(SCHEMA_SQL)

    @classmethod
    def tearDownClass(cls):
        try:
            with connection.cursor() as cursor:
                cursor.execute(TEARDOWN_SQL)
        finally:
            super().tearDownClass()

    def test_profiles_crud(self):
        with connection.cursor() as cursor:
            # CREATE
            cursor.execute(
                """
                INSERT INTO profiles (sex, sexual_preferences, biography, list_of_interests, fame, longitude, latitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                [
                    "male",
                    "female",
                    "Hello from raw SQL",
                    ["music", "travel"],
                    10,
                    30.523400,
                    50.450100,
                ],
            )
            profile_id = cursor.fetchone()[0]

            # READ
            cursor.execute(
                "SELECT sex, sexual_preferences, biography, fame FROM profiles WHERE id = %s",
                [profile_id],
            )
            row = cursor.fetchone()
            self.assertEqual(row, ("male", "female", "Hello from raw SQL", 10))

            # UPDATE
            cursor.execute(
                "UPDATE profiles SET fame = %s WHERE id = %s",
                [99, profile_id],
            )
            cursor.execute("SELECT fame FROM profiles WHERE id = %s", [profile_id])
            self.assertEqual(cursor.fetchone()[0], 99)

            # DELETE
            cursor.execute("DELETE FROM profiles WHERE id = %s", [profile_id])
            cursor.execute("SELECT COUNT(*) FROM profiles WHERE id = %s", [profile_id])
            self.assertEqual(cursor.fetchone()[0], 0)

    def test_users_and_images_crud(self):
        with connection.cursor() as cursor:
            # Create a profile to reference
            cursor.execute(
                """
                INSERT INTO profiles (sex, sexual_preferences, biography, list_of_interests, fame)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                ["female", "male", "Profile for user", ["books"], 1],
            )
            profile_id = cursor.fetchone()[0]

            # CREATE user
            cursor.execute(
                """
                INSERT INTO users (profile_id, name, surname, email, password)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                [profile_id, "Test", "User", "test.user@example.com", "password123"],
            )
            user_id = cursor.fetchone()[0]

            # CREATE image (avatar)
            cursor.execute(
                """
                INSERT INTO images (profile_id, image_url, is_avatar)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                [profile_id, "https://picsum.photos/seed/test/600/600", True],
            )
            image_id = cursor.fetchone()[0]

            # READ join
            cursor.execute(
                """
                SELECT u.id, u.email, p.sex, i.id, i.is_avatar
                FROM users u
                JOIN profiles p ON p.id = u.profile_id
                JOIN images i ON i.profile_id = p.id
                WHERE u.id = %s
                """,
                [user_id],
            )
            row = cursor.fetchone()
            self.assertEqual(row, (user_id, "test.user@example.com", "female", image_id, True))

            # UPDATE user
            cursor.execute("UPDATE users SET surname = %s WHERE id = %s", ["User2", user_id])
            cursor.execute("SELECT surname FROM users WHERE id = %s", [user_id])
            self.assertEqual(cursor.fetchone()[0], "User2")

            # DELETE image then user (or rely on cascade via profile delete)
            cursor.execute("DELETE FROM images WHERE id = %s", [image_id])
            cursor.execute("SELECT COUNT(*) FROM images WHERE id = %s", [image_id])
            self.assertEqual(cursor.fetchone()[0], 0)

            cursor.execute("DELETE FROM users WHERE id = %s", [user_id])
            cursor.execute("SELECT COUNT(*) FROM users WHERE id = %s", [user_id])
            self.assertEqual(cursor.fetchone()[0], 0)
