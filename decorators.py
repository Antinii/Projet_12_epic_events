from functools import wraps
from permissions import has_permission
from auth import get_logged_in_user


def permission_required(permission):
    """
    A decorator to check if a user has the required permission to execute a function.

    Args:
        permission (str): The required permission for the function.

    Returns:
        function: The wrapped function which includes the permission check.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import session_manager
            user = get_logged_in_user(session_manager.get_current_token())
            if not user:
                print("You are no longer logged in, please login again.\n")
                return
            if not has_permission(user, permission):
                print("\nYou don't have the permission to access this ressource.\n")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator
