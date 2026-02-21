# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Matcha is a Django-based dating application backend using PostgreSQL. This is a **learning project** focused on understanding Django and backend development fundamentals.

**Key Learning Goals:**
- Building a REST API with Django without using Django ORM
- Implementing n-layer architecture (endpoints → services → repositories)
- Working with raw SQL queries
- Understanding backend architecture patterns

The project uses raw SQL queries instead of Django ORM models to interact with a custom database schema.

## Database Architecture

The database has three main tables with specific relationships:
- `profiles` - User profile information (sex, sexual preferences, biography, interests, fame rating, geolocation)
- `users` - User account data with 1:1 relationship to profiles via `profile_id` (FK with ON DELETE CASCADE)
- `images` - Profile images with 1:N relationship to profiles (each profile can have multiple images but only one avatar, enforced by partial unique index)

The schema is defined in `db/init/00_schema.sql` which includes seed data with 10 test users.

## Development Commands

### Database Setup

Start PostgreSQL and pgAdmin containers:
```bash
docker compose up -d db pgadmin
```

Check container status:
```bash
docker compose ps
```

Stop containers:
```bash
docker compose down
```

**Full database reset** (drops volume and re-initializes from `db/init/00_schema.sql`):
```bash
docker compose down -v
docker compose up -d db pgadmin
```

Apply SQL manually to running database (without volume reset):
```bash
docker compose exec -T db psql -U matcha -d matcha_test -f /docker-entrypoint-initdb.d/00_schema.sql
```

Connect to PostgreSQL via psql inside container:
```bash
docker compose exec -T db psql -U matcha -d matcha_test
```

### Database Connection Details

- **Database**: `matcha_test`
- **User**: `matcha`
- **Password**: `matcha_password`
- **Host (from host machine)**: `localhost`
- **Port (from host machine)**: `5433` (configurable via `DB_PORT` env var)
- **Host (from within Docker network)**: `db`
- **Port (from within Docker network)**: `5432`

### pgAdmin Access

URL: `http://localhost:8080` (configurable via `PGADMIN_PORT`)
- Email: `admin@matcha.local`
- Password: `admin_password`

### Django Development

All Django commands run from the `backend/` directory.

Setup virtual environment:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run development server:
```bash
python manage.py runserver
```

Run all tests:
```bash
python manage.py test
```

Run specific test class:
```bash
python manage.py test hello.tests.RawSqlCrudTests
```

Run specific test method:
```bash
python manage.py test hello.tests.RawSqlCrudTests.test_profiles_crud
```

## Configuration

Django settings use `django-environ` to read environment variables from `backend/.env` (optional file). The following environment variables can be configured:

- `DEBUG` (default: `True`)
- `SECRET_KEY` (default: `'django-insecure-change-me'`)
- `ALLOWED_HOSTS` (default: `[]`)
- `DATABASE_URL` (if set, overrides individual DB_* variables)
- `DB_NAME` (default: `'matcha_test'`)
- `DB_USER` (default: `'matcha'`)
- `DB_PASSWORD` (default: `'matcha_password'`)
- `DB_HOST` (default: `'localhost'`)
- `DB_PORT` (default: `5433`)

Settings file: `backend/config/settings.py`

## Code Patterns

### Raw SQL Usage

This project **does not use Django ORM models**. All database interactions use raw SQL via `django.db.connection.cursor()`.

Example pattern from `backend/hello/views.py:13-32`:
```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute(
        """
        SELECT id, profile_id, name, surname, email
        FROM users
        ORDER BY id
        """
    )
    rows = cursor.fetchall()
```

### Testing with Raw SQL

Tests are in `backend/hello/tests.py` using `TransactionTestCase`. The test class creates the schema in `setUpClass()` and drops it in `tearDownClass()`:

- Schema creation uses `SCHEMA_SQL` constant (matches `db/init/00_schema.sql` structure)
- Tests use `connection.cursor()` for all database operations
- `TEARDOWN_SQL` drops tables with CASCADE to clean up

## Project Structure

```
matcha/
├── backend/
│   ├── config/          # Django project settings
│   │   ├── settings.py  # Environment-based configuration
│   │   └── urls.py      # URL routing
│   ├── hello/           # Main Django app
│   │   ├── views.py     # Views using raw SQL
│   │   └── tests.py     # Raw SQL CRUD tests
│   ├── manage.py        # Django CLI
│   └── requirements.txt # Python dependencies
├── db/
│   └── init/
│       └── 00_schema.sql # PostgreSQL schema + seed data
└── docker-compose.yml   # PostgreSQL + pgAdmin services
```

## Planned Architecture

The project will follow **n-layer architecture** without Django ORM:

```
Views (endpoints)
    ↓
Services (business logic)
    ↓
Repositories (data access layer with raw SQL)
    ↓
Database
```

**Future structure:**
```
backend/
├── api/              # Django app for API endpoints
│   ├── views/        # Request handlers (endpoints)
│   ├── serializers/  # Request/response validation
│   └── urls.py       # URL routing
├── services/         # Business logic layer
│   ├── user_service.py
│   ├── profile_service.py
│   └── ...
├── repositories/     # Data access layer (raw SQL)
│   ├── user_repository.py
│   ├── profile_repository.py
│   └── ...
└── models/           # Data classes (not ORM models)
    └── ...
```

See `ROADMAP.md` for detailed implementation plans.

## Important Notes

- Database init scripts in `db/init/` only run on **first volume creation**. To apply schema changes, either reset the volume with `docker compose down -v` or manually execute SQL files.
- The Django project uses `config` as the settings module name (not the typical project name).
- Port 5433 is used for PostgreSQL on the host to avoid conflicts with system PostgreSQL installations.
- This is a learning project - code may be refactored frequently as new patterns are discovered.
