from functools import wraps
from permissions import has_permission
from auth import get_logged_in_user


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from views.employees_view import current_token
            user = get_logged_in_user(current_token)
            if not user:
                print("You are no longer logged in, please login again.\n")
                return
            if not has_permission(user, permission):
                print("\nYou don't have the permission to access this ressource.\n")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator
