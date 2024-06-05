import getpass
from controllers.employees_controller import create_employee, get_employees
from controllers.departments_controller import get_departments
from controllers.employees_controller import login_employee, create_employee, update_employee, delete_employee
from models.employees import Employee
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from views.contracts_view import manage_contracts_menu
from views.customers_view import manage_customers_menu
from views.events_view import manage_events_menu
from config.auth import get_logged_in_user
from config.settings import DATABASE_URL
from rich.console import Console
from rich.table import Table
from config.decorators import permission_required
import config.session_manager as session_manager

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def manage_employees_menu():
    """
    Display for employees menu.
    """
    console = Console()

    while True:
        table = Table(show_header=True, header_style="bold green")
        table.add_column("Employees menu, please select an option: ", justify="left", style="cyan", no_wrap=True)
        
        table.add_row("1. Create a new employee")
        table.add_row("2. Show all the employees")
        table.add_row("3. Update an employee")
        table.add_row("4. Delete an employee")
        table.add_row("5. Go back")

        console.print(table)

        choice = input("Enter your choice: ")

        if choice == '1':
            create_new_employee()
        elif choice == '2':
            get_employees()
        elif choice == '3':
            update_employee_view()
        elif choice == '4':
            delete_employee_view()
        elif choice == '5':
            break
        else:
            console.print("\nInvalid choice, try again\n", style="bold red")

def logged_in_menu(name):
    """
    Display the main menu of the application.
    """
    console = Console()

    while True:
        table = Table(show_header=True, header_style="bold green")

        table.add_column(f"Welcome {name}, please choose an option:", justify="left", style="cyan", no_wrap=True)
        
        table.add_row("1. Manage Employees")
        table.add_row("2. Manage Customers")
        table.add_row("3. Manage Contracts")
        table.add_row("4. Manage Events")
        table.add_row("5. Logout")

        console.print(table)

        choice = input("Enter your choice: ")

        if choice == '1':
            manage_employees_menu()
        elif choice == '2':
            manage_customers_menu()
        elif choice == '3':
            manage_contracts_menu()
        elif choice == '4':
            manage_events_menu()
        elif choice == '5':
            print(f"Goodbye, {name}!")
            break
        else:
            console.print("\nInvalid choice, try again\n", style="bold red")

def display_departments(departments):
    """
    Display a list of departments.

    Args:
        departments (list): List of departments to display.
    """
    console = Console()

    table = Table(title="List of all Departments", show_header=True, header_style="magenta", show_lines=True)

    table.add_column("ID", justify="center")
    table.add_column("Department Name", justify="left")

    for dept in departments:
        table.add_row(str(dept.id), dept.name)

    console.print(table)

def create_user_view():
    """
    Display a form to create a new user and save it to the database.

    This function prompts the user to input their name, password, and department. 
    It ensures the password is confirmed correctly, lists the available departments, 
    and calls create_employee to save the new user's details to the database.

    Inputs:
        name (str): The name of the user.
        password (str): The password of the user.
        password_confirm (str): The confirmation of the password.
        department_id (int): The ID of the department the user belongs to.

    Outputs:
        str: Result message indicating the success or failure of the user creation.
    """
    console = Console()
    name = input("Enter your name: ")

    while True:
        password = getpass.getpass("Enter your password: ")
        password_confirm = getpass.getpass("Confirm your password: ")
        if password == password_confirm:
            break
        else:
            console.print("Passwords do not match. Please try again.", style="bold red")

    departments = get_departments()
    display_departments(departments)
    department_id = input("Please select your department ID: ")
    result = create_employee(name, password, department_id)
    print(result)

def login_view():
    """
    Display the login form and handle user authentication.

    This function prompts the user to input their name and password. It calls the 
    login_employee function to verify the credentials. If the login is successful, 
    it sets the current session token and displays the main menu for the logged-in user. 
    If the login fails, it displays an error message and prompts the user to try again.

    Inputs:
        name (str): The name of the user.
        password (str): The password of the user.
    """
    while True:
        name = input("Enter your name: ")
        password = getpass.getpass("Enter your password: ")
        result = login_employee(name, password)
        if result["message"] == "Login successful":
            session_manager.set_current_token(result["token"])
            # print(f"Token: {session_manager.get_current_token()}") # Check if the token is generated correctly
            logged_in_menu(name)
            break
        else:
            print(result["message"])

@permission_required('create_employees')
def create_new_employee():
    """
    Create a new employee in the database.

    This function prompts the user to input the necessary information to create a new employee, 
    including name, password, and department ID. It then calls the create_employee function 
    to save the new employee to the database.

    Permissions:
        Requires 'create_employees' permission.

    Inputs:
        name (str): The name of the employee.
        password (str): The password of the employee.
        department_id (int): The ID of the department to which the employee belongs.

    Outputs:
        str: Result message indicating the success or failure of the employee creation.
    """
    console = Console()
    user = get_logged_in_user(session_manager.get_current_token())
    if not user:
        console.print("Please login.", style="bold red")
        return
    
    name = input("Enter the employee name: ")

    while True:
        password = getpass.getpass("Enter the employee password: ")
        password_confirm = getpass.getpass("Confirm the password: ")
        if password == password_confirm:
            break
        else:
            console.print("Passwords do not match. Please try again.", style="bold red")

    departments = get_departments()
    display_departments(departments)
    department_id = input("Please select the employee department ID: ")
    result = create_employee(name, password, department_id)
    print(result)

@permission_required('update_employees')
def update_employee_view():
    """
    Update an existing employee in the database.

    This function lists the current employees and prompts the user to select an employee to update. 
    It then prompts the user to input new values for the employee's name, password, and department ID, 
    and calls the update_employee function to save the changes to the database.

    Permissions:
        Requires 'update_employees' permission.

    Inputs:
        employee_id (int): The ID of the employee to update.
        name (str, optional): The new name of the employee.
        password (str, optional): The new password of the employee.
        department_id (int, optional): The new department ID of the employee.

    Outputs:
        str: Result message indicating the success or failure of the employee update.
    """
    console = Console()
    while True:
        print("Choose the employee to update:")
        get_employees()

        employee_id = (input("Enter the employee ID to update: "))
        if not employee_id.isdigit():
            console.print("Please enter a valid numeric ID.", style="bold red")
            continue
        employee_id = int(employee_id)
        employee = session.query(Employee).get(employee_id)
        if not employee:
            console.print("Employee ID not found. Please choose an existing ID from the list.", style="bold red")
            continue

        name = input("Enter new name (leave blank to keep current): ")

        password = None
        while True:
            new_password = getpass.getpass("Enter new password (leave blank to keep current): ")
            if new_password:
                password_confirm = getpass.getpass("Confirm the new password: ")
                if new_password == password_confirm:
                    password = new_password
                    break
                else:
                    console.print("Passwords do not match. Please try again.", style="bold red")
            else:
                break

        departments = get_departments()
        display_departments(departments)
        department_id = input("Enter new department ID (leave blank to keep current): ")

        department_id = int(department_id) if department_id else None

        result = update_employee(employee_id, name if name else None, password if password else None, department_id)
        print(result)
        break

@permission_required('delete_employees')
def delete_employee_view():
    """
    Delete an existing employee from the database.

    This function lists the current employees and prompts the user to select an employee to delete. 
    It then asks for confirmation before calling the delete_employee function to remove the employee 
    from the database.

    Permissions:
        Requires 'delete_employees' permission.

    Inputs:
        employee_id (int): The ID of the employee to delete.

    Outputs:
        str: Result message indicating the success or failure of the employee deletion.
    """
    console = Console()

    while True:
        print("List of all employees:")
        get_employees()

        employee_id = (input("Enter the employee ID to update: "))
        if not employee_id.isdigit():
            console.print("Please enter a valid numeric ID.", style="bold red")
            continue

        employee_id = int(employee_id)
        employee = session.query(Employee).get(employee_id)
        if not employee:
            console.print("Employee ID not found. Please choose an existing ID from the list.", style="bold red")
            continue

        confirmation = input(f"Are you sure you want to delete the employee with ID {employee_id}? (yes/no): ")
        if confirmation.lower() == 'yes':
            result = delete_employee(employee_id)
            print(result)
        else:
            console.print("Deletion cancelled.", style="bold red")
        break
