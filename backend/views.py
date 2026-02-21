import logging
import json

from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from services import UserService
from dto import CreateUserDTO, UpdateUserDTO
from exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    InvalidUserDataException,
    ProfileNotFoundException,
    InvalidVerificationToken,
)
  
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
                SELECT id, profile_id, name, surname, email, is_verified
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
        {"id": r[0], "profile_id": r[1], "name": r[2], "surname": r[3], "email": r[4], "is_verified": r[5] if len(r) > 5 else False}
        for r in rows
    ]

    logger.info("Fetched %s users via raw SQL: %s", len(users), users)
    return JsonResponse({"ok": True, "count": len(users), "users": users})


# ========================================
# N-Layer Architecture Endpoints
# ========================================

@csrf_exempt
@require_http_methods(["GET", "POST"])
def user_list_create(request):
    """
    Handle GET (list users) and POST (create user) requests.
    """
    service = UserService()

    if request.method == "GET":
        return _handle_list_users(request, service)
    elif request.method == "POST":
        return _handle_create_user(request, service)


@require_http_methods(["GET"])
def verify_email(request):
    """
    GET /api/auth/verify-email/?token=... - Verify email by token, return auth_token and redirect_url.
    """
    token = request.GET.get("token")
    if not token or not token.strip():
        return JsonResponse(
            {"error": "Missing or empty verification token"},
            status=400,
        )
    try:
        service = UserService()
        result = service.authorize_user_by_token(token)
        return JsonResponse(result, status=200)
    except InvalidVerificationToken as e:
        logger.warning("Invalid verification token: %s", e.message)
        return JsonResponse(
            {"error": e.message or "Invalid verification token"},
            status=400,
        )
    except UserNotFoundException as e:
        logger.warning("User not found for verification: %s", e.user_id)
        return JsonResponse(
            {"error": f"User with id={e.user_id} not found"},
            status=400,
        )


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def user_detail(request, user_id):
    """
    Handle GET (retrieve), PUT (update), and DELETE (delete) for a specific user.
    """
    service = UserService()

    if request.method == "GET":
        return _handle_get_user(user_id, service)
    elif request.method == "PUT":
        return _handle_update_user(request, user_id, service)
    elif request.method == "DELETE":
        return _handle_delete_user(user_id, service)


# ========================================
# Helper Functions
# ========================================

def _handle_list_users(request, service: UserService) -> JsonResponse:
    """
    GET /api/users/ - List users with pagination.
    """
    try:
        # Parse query parameters
        limit = int(request.GET.get('limit', 100))
        offset = int(request.GET.get('offset', 0))

        users = service.list_users(limit=limit, offset=offset)
        users_data = [user.to_dict() for user in users]

        logger.info(f"Listed {len(users_data)} users (limit={limit}, offset={offset})")
        return JsonResponse({'users': users_data}, status=200)

    except Exception as e:
        logger.error(f"Error listing users: {e}", exc_info=True)
        return JsonResponse({'error': 'Internal server error'}, status=500)


def _handle_create_user(request, service: UserService) -> JsonResponse:
    """
    POST /api/users/ - Create a new user.
    """
    try:
        # Parse JSON body
        data = json.loads(request.body)

        # Create DTO
        create_dto = CreateUserDTO(
            profile_id=data.get('profile_id'),
            name=data.get('name'),
            surname=data.get('surname'),
            email=data.get('email'),
            password=data.get('password')
        )

        # Create user
        user = service.create_user(create_dto)
        logger.info(f"Created user: {user.email} (id={user.id})")

        return JsonResponse(user.to_dict(), status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except InvalidUserDataException as e:
        logger.warning(f"Invalid user data: {e.errors}")
        return JsonResponse({'error': 'Validation failed', 'details': e.errors}, status=400)

    except UserAlreadyExistsException as e:
        logger.warning(f"User already exists: {e.email}")
        return JsonResponse({'error': f"User with email '{e.email}' already exists"}, status=409)

    except ProfileNotFoundException as e:
        logger.warning(f"Profile not found: {e.profile_id}")
        return JsonResponse({'error': f"Profile with id={e.profile_id} not found"}, status=400)

    except Exception as e:
        logger.error(f"Error creating user: {e}", exc_info=True)
        return JsonResponse({'error': 'Internal server error'}, status=500)


def _handle_get_user(user_id: int, service: UserService) -> JsonResponse:
    """
    GET /api/users/{id}/ - Retrieve a specific user.
    """
    try:
        user = service.get_user(user_id)
        logger.info(f"Retrieved user: {user.email} (id={user.id})")
        return JsonResponse(user.to_dict(), status=200)

    except UserNotFoundException as e:
        logger.warning(f"User not found: {e.user_id}")
        return JsonResponse({'error': f"User with id={e.user_id} not found"}, status=404)

    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {e}", exc_info=True)
        return JsonResponse({'error': 'Internal server error'}, status=500)


def _handle_update_user(request, user_id: int, service: UserService) -> JsonResponse:
    """
    PUT /api/users/{id}/ - Update a user.
    """
    try:
        # Parse JSON body
        data = json.loads(request.body)

        # Create DTO
        update_dto = UpdateUserDTO(
            name=data.get('name'),
            surname=data.get('surname'),
            email=data.get('email'),
            password=data.get('password')
        )

        # Update user
        user = service.update_user(user_id, update_dto)
        logger.info(f"Updated user: {user.email} (id={user.id})")

        return JsonResponse(user.to_dict(), status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except UserNotFoundException as e:
        logger.warning(f"User not found: {e.user_id}")
        return JsonResponse({'error': f"User with id={e.user_id} not found"}, status=404)

    except InvalidUserDataException as e:
        logger.warning(f"Invalid user data: {e.errors}")
        return JsonResponse({'error': 'Validation failed', 'details': e.errors}, status=400)

    except UserAlreadyExistsException as e:
        logger.warning(f"Email already taken: {e.email}")
        return JsonResponse({'error': f"Email '{e.email}' is already taken"}, status=409)

    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}", exc_info=True)
        return JsonResponse({'error': 'Internal server error'}, status=500)


def _handle_delete_user(user_id: int, service: UserService) -> JsonResponse:
    """
    DELETE /api/users/{id}/ - Delete a user.
    """
    try:
        deleted = service.delete_user(user_id)

        if deleted:
            logger.info(f"Deleted user: id={user_id}")
            return JsonResponse({'deleted': True}, status=200)
        else:
            logger.warning(f"User not found for deletion: id={user_id}")
            return JsonResponse({'error': f"User with id={user_id} not found"}, status=404)

    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}", exc_info=True)
        return JsonResponse({'error': 'Internal server error'}, status=500)