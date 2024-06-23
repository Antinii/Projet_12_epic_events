from functools import wraps
from config.permissions import has_permission
from config.auth import get_logged_in_user, logout
import config.session_manager as session_manager
from rich.console import Console
from rich.text import Text


def permission_required(permission):
    """
    A decorator to check if a user has the required permission to execute a function.

    Args:
        permission (str): The required permission for the function.

    Returns:
        function: The wrapped function which includes the permission check.
    """
    console = Console()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = session_manager.get_current_token()
            user, is_expired = get_logged_in_user(token)
            if is_expired:
                text = Text("\n Your session has expired, please login again. \n")
                text.stylize("bold red")
                console.print(text)
                logout()
                return
            if not user:
                text = Text("\n You are no longer logged in, please login again. \n")
                text.stylize("bold red")
                console.print(text)
                logout()
                return
            if not has_permission(user, permission):
                text = Text("\n You don't have the permission to access this ressource. \n")
                text.stylize("bold red")
                console.print(text)
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator
