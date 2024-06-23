from config.settings import SECRET_KEY, DATABASE_URL
from models.employees import Employee
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import config.session_manager as session_manager
import jwt
import datetime


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def generate_token(employee_id):
    """
    Generates a JWT token with a 1-hour expiry for the given employee_id.

    Args:
        employee_id (int): The ID of the employee for whom the token is generated.

    Returns:
        str: JWT token encoded with the employee ID.
    """
    payload = {
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'sub': employee_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_token(token):
    """
    Decodes the provided JWT token using the SECRET_KEY.

    Args:
        token (str): The JWT token to decode.

    Returns:
        tuple: A tuple containing:
            - int or None: The employee ID extracted from the token.
            - bool: True if the token has expired, False otherwise.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub'], False
    except jwt.ExpiredSignatureError:
        return None, True
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


def get_logged_in_user(token):
    """
    Retrieves the logged-in employee based on the provided JWT token.

    Args:
        token (str): The JWT token to identify the logged-in user.

    Returns:
        tuple: A tuple containing:
            - Employee or None: The Employee object of the logged-in user, if found.
            - bool: True if the token has expired, False otherwise.
    """
    employee_id, is_expired = decode_token(token)
    if employee_id:
        return session.query(Employee).filter_by(id=employee_id).first(), is_expired
    return None, is_expired


def logout():
    """
    Clears the current session token and redirects to the main view.

    This function clears the current session token using session_manager.clear_current_token(),
    and then redirects the user to the main view for further actions.
    """
    session_manager.clear_current_token()
    from views.main_view import main
    main()
