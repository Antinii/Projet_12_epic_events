from datetime import datetime
import getpass
from rich.console import Console


def get_valid_date(prompt, allow_blank=False):
    """
    Prompts the user for a date input in YYYY-MM-DD format and validates it.

    Args:
        prompt (str): The prompt message to display to the user.
        allow_blank (bool, optional): If True, allows the input to be blank (None returned). Default is False.

    Returns:
        datetime.date or None: The validated date object parsed from input, or None if input is
        blank and allow_blank is True.
    """
    console = Console()
    while True:
        date_input = input(prompt)
        if allow_blank and date_input == "":
            return None
        try:
            return datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            console.print("Invalid date format. Please enter the date in YYYY-MM-DD format.", style="bold red")


def get_valid_int(prompt, allow_blank=False):
    """
    Prompts the user for an integer input and validates it.

    Args:
        prompt (str): The prompt message to display to the user.
        allow_blank (bool, optional): If True, allows the input to be blank (None returned). Default is False.

    Returns:
        int or None: The validated integer parsed from input, or None if input is blank and allow_blank is True.
    """
    console = Console()
    while True:
        input_value = input(prompt)
        if allow_blank and input_value == "":
            return None
        if input_value.isdigit():
            return int(input_value)
        console.print("Please enter a valid numeric value.", style="bold red")


def get_valid_float(prompt, allow_blank=False):
    """
    Prompts the user for a float input and validates it.

    Args:
        prompt (str): The prompt message to display to the user.
        allow_blank (bool, optional): If True, allows the input to be blank (None returned). Default is False.

    Returns:
        float or None: The validated float parsed from input, or None if input is blank and allow_blank is True.

    """
    console = Console()
    while True:
        input_value = input(prompt)
        if allow_blank and input_value == "":
            return None
        try:
            return float(input_value)
        except ValueError:
            console.print("Please enter a valid numeric value.", style="bold red")


def get_valid_id(session, prompt, get_function, entity_name, allow_blank=False, current_id=None):
    """
    Prompts the user for an entity ID input, validates it against the provided SQLAlchemy session and entity type.

    Args:
        session (sqlalchemy.orm.Session): The SQLAlchemy session object for querying the database.
        prompt (str): The prompt message to display to the user.
        get_function (function): A function to fetch entities from the session.
        entity_name (class): The SQLAlchemy entity class name to query.
        allow_blank (bool, optional): If True, allows the input to be blank (current_id returned). Default is False.
        current_id (int or None, optional): The current ID value to return if input is blank and allow_blank is True.
        Default is None.

    Returns:
        int or None: The validated entity ID parsed from input, or None if input is blank and allow_blank is True.

    """
    console = Console()
    while True:
        get_function(session)
        input_id = input(prompt)
        if allow_blank and input_id == "":
            return current_id
        if input_id.isdigit():
            entity_id = int(input_id)
            entity = session.query(entity_name).get(entity_id)
            if entity:
                return entity_id
            else:
                console.print(f"{entity_name.__name__} ID not found. Please choose an existing ID from the list.",
                              style="bold red")
        else:
            console.print("Please enter a valid numeric ID.", style="bold red")


def get_valid_password():
    """
    Prompts the user for a password input, validates its length and confirmation.

    Returns:
        str: The validated password string.
    """
    console = Console()
    while True:
        password = getpass.getpass("Enter the password (minimum 6 characters): ")
        if len(password) < 6:
            console.print("Password must be at least 6 characters long. Please try again.", style="bold red")
            continue
        password_confirm = getpass.getpass("Confirm the password: ")
        if password == password_confirm:
            return password
        else:
            console.print("Passwords do not match. Please try again.", style="bold red")


def get_valid_name(min_length=3):
    """
    Prompts the user for a name input and validates its length.

    Args:
        min_length (int, optional): Minimum required length for the name. Default is 3.

    Returns:
        str: The validated name string.
    """
    console = Console()
    while True:
        name = input(f"Enter your name (minimum {min_length} characters): ")
        if len(name) >= min_length:
            return name
        else:
            console.print(f"Name must be at least {min_length} characters long. Please try again.", style="bold red")
