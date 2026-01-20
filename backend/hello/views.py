import logging

from django.db import connection
from django.http import HttpResponse, JsonResponse
  
def index(request):
    return HttpResponse("Hello World")


logger = logging.getLogger(__name__)


def users_list(request):
    """
    Raw SQL: fetch all users from custom `users` table and log them.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, profile_id, name, surname, email
                FROM users
                ORDER BY id
                """
            )
            rows = cursor.fetchall()
    except Exception:
        logger.exception("Failed to fetch users via raw SQL")
        return JsonResponse(
            {"ok": False, "error": "Failed to fetch users (is the `users` table present in DB?)"},
            status=500,
        )

    users = [
        {"id": r[0], "profile_id": r[1], "name": r[2], "surname": r[3], "email": r[4]}
        for r in rows
    ]

    logger.info("Fetched %s users via raw SQL: %s", len(users), users)
    return JsonResponse({"ok": True, "count": len(users), "users": users})