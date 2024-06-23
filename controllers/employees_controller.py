from config.settings import DATABASE_URL
from models.employees import Employee
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config.auth import generate_token
from rich.console import Console
from rich.table import Table
from sentry_sdk import capture_message, capture_exception

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def create_employee(session, name, password, department_id):
    """
    Create an employee in the database.
    Create a log in sentry when an employee is created successfully.
    """
    try:
        name = name.strip()
        password = password.strip()
        if not name or not password:
            return "Name and password cannot be empty."
        if session.query(Employee).filter_by(name=name).first():
            return "This employee already exists, please choose another one."
        new_employee = Employee(name=name, department_id=department_id)
        new_employee.set_password(password)
        session.add(new_employee)
        session.commit()
        capture_message(f"Employee created: {name}", level="info")
        return "User created successfully!"
    except Exception as e:
        session.rollback()
        capture_exception(e)
        return "Error creating employee."


def login_employee(session, name, password):
    """
    Attempts to log in an employee by validating the provided name and password.
    """
    name = name.strip()
    password = password.strip()
    employee = session.query(Employee).filter_by(name=name).first()
    if not employee:
        return {"message": "\n Username does not exist, please try again. \n"}
    if employee.check_password(password):
        token = generate_token(employee.id)
        return {"message": "Login successful", "token": token}
    else:
        return {"message": "\n Incorrect password, please try again. \n"}


def get_employees(session):
    """
    Show all employees in a nice table format.
    """
    console = Console()
    employees = session.query(Employee).all()

    if not employees:
        print("No employees found.")
        return

    table = Table(title="List of all Employees", show_header=True, header_style="magenta", show_lines=True)

    table.add_column("ID", justify="center")
    table.add_column("Name", justify="left")
    table.add_column("Department", justify="left")

    for employee in employees:
        table.add_row(str(employee.id), employee.name, employee.department.name)

    console.print(table)


def update_employee(session, employee_id, name=None, password=None, department_id=None):
    """
    Update an existing employee in the database.
    Create a log in sentry when an employee is updated successfully.
    """
    try:
        employee = session.get(Employee, employee_id)
        if not employee:
            return "Employee not found."
        if name:
            employee.name = name.strip()
        if password:
            employee.set_password(password.strip())
        if department_id:
            employee.department_id = department_id
        session.commit()
        capture_message(f"Employee updated: {name}", level="info")
        return "Employee updated successfully!"
    except Exception as e:
        session.rollback()
        capture_exception(e)
        return "Error updating employee."


def delete_employee(session, employee_id):
    """
    Delete an employee in the database.
    """
    employee = session.get(Employee, employee_id)
    if not employee:
        return "Employee not found."
    session.delete(employee)
    session.commit()
    return "Employee deleted successfully!"
