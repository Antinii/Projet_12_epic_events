import getpass
from controllers.employees_controller import create_employee, get_employees
from controllers.departments_controller import get_departments
from controllers.departments_controller import get_departments
from controllers.employees_controller import login_employee, create_employee, update_employee, delete_employee
from models.employees import Employee
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contracts_view import manage_contracts_menu
from customers_view import manage_customers_menu
from events_view import manage_events_menu
from auth import get_logged_in_user
from settings import DATABASE_URL
from texttable import Texttable
from decorators import permission_required
import session_manager

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def manage_employees_menu():
    """
    Display for employees menu.
    """
    while True:
        table = Texttable()
        table.header(["Employees menu, please select an option"])
        table.add_row(["1. Create a new employee"])
        table.add_row(["2. Show all the employees"])
        table.add_row(["3. Update an employee"])
        table.add_row(["4. Delete an employee"])
        table.add_row(["5. Go back"])
        print(table.draw())

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
            print("Invalid choice")

def logged_in_menu(name):
    """
    Display the main menu of the application.
    """
    while True:
        table = Texttable()
        table.header([f"Welcome {name}, please choose an option:"])
        table.add_row(["1. Manage Employees"])
        table.add_row(["2. Manage Customers"])
        table.add_row(["3. Manage Contracts"])
        table.add_row(["4. Manage Events"])
        table.add_row(["5. Logout"])
        print(table.draw())

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
            print("Invalid choice")

def display_departments(departments):
    """
    Display a list of departments.

    Args:
        departments (list): List of departments to display.
    """
    table = Texttable()
    table.header(["ID", "Department Name"])
    for dept in departments:
        table.add_row([dept.id, dept.name])
    print(table.draw())

def create_user_view():
    name = input("Enter your name: ")

    while True:
        password = getpass.getpass("Enter your password: ")
        password_confirm = getpass.getpass("Confirm your password: ")
        if password == password_confirm:
            break
        else:
            print("Passwords do not match. Please try again.")

    departments = get_departments()
    display_departments(departments)
    department_id = input("Please select your department ID: ")
    result = create_employee(name, password, department_id)
    print(result)

def login_view():
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
    user = get_logged_in_user(session_manager.get_current_token())
    if not user:
        print("Please login.")
        return
    
    name = input("Enter the employee name: ")

    while True:
        password = getpass.getpass("Enter the employee password: ")
        password_confirm = getpass.getpass("Confirm the password: ")
        if password == password_confirm:
            break
        else:
            print("Passwords do not match. Please try again.")

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
    while True:
        print("Choose the employee to update:")
        get_employees()

        employee_id = (input("Enter the employee ID to update: "))
        if not employee_id.isdigit():
            print("Please enter a valid numeric ID.")
            continue
        employee_id = int(employee_id)
        employee = session.query(Employee).get(employee_id)
        if not employee:
            print("Employee ID not found. Please choose an existing ID from the list.")
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
                    print("Passwords do not match. Please try again.")
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
    while True:
        print("List of all employees:")
        get_employees()

        employee_id = (input("Enter the employee ID to update: "))
        if not employee_id.isdigit():
            print("Please enter a valid numeric ID.")
            continue

        employee_id = int(employee_id)
        employee = session.query(Employee).get(employee_id)
        if not employee:
            print("Employee ID not found. Please choose an existing ID from the list.")
            continue

        confirmation = input(f"Are you sure you want to delete the employee with ID {employee_id}? (yes/no): ")
        if confirmation.lower() == 'yes':
            result = delete_employee(employee_id)
            print(result)
        else:
            print("Deletion cancelled.")
        break
