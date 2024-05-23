import getpass
from controllers.employees_controller import create_employee, get_employees, Session
from controllers.departments_controller import get_departments
from controllers.departments_controller import get_departments
from controllers.employees_controller import login_employee, create_employee
from views.customers_view import manage_customers_menu
# from views.contracts_view import manage_contracts_menu
from texttable import Texttable
from decorators import permission_required

current_token = None

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
            get_employees(Session())
        elif choice == '3':
            pass
        elif choice == '4':
            pass
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
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            print(f"Goodbye, {name}!")
            break
        else:
            print("Invalid choice")


@permission_required('create_employees')
def create_new_employee():
    """
    Create a new employee in the database.
    """
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

def display_departments(departments):
    table = Texttable()
    table.header(["ID", "Department Name"])
    for dept in departments:
        table.add_row([dept.id, dept.name])
    print(table.draw())

def create_employee_view():
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
    global current_token
    name = input("Enter your name: ")
    password = getpass.getpass("Enter your password: ")
    result = login_employee(name, password)
    if result["message"] == "Login successful":
        current_token = result["token"]
        # print(f"Token: {current_token}") Check if the token is generated correctly
        logged_in_menu(name)
    else:
        print(result["message"])
