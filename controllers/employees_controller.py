from models.employees import Employee
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from auth import generate_token
from texttable import Texttable

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
session = Session()

def create_employee(name, password, department_id):
    if session.query(Employee).filter_by(name=name).first():
        return "This employee already exists, please choose another one."
    new_employee = Employee(name=name, department_id=department_id)
    new_employee.set_password(password)
    session.add(new_employee)
    session.commit()
    return "User created successfully !!!"

def login_employee(name, password):
    employee = session.query(Employee).filter_by(name=name).first()
    if not employee:
        return "Username does not exist, please try again."
    if employee.check_password(password):
        token = generate_token(employee.id)
        return {"message": "Login successful", "token": token}
    else:
        return "\n Incorrect password, please try again. \n"

def get_employees(session):
    """
    Show all employees in a nice table format.
    """
    employees = session.query(Employee).all()

    if not employees:
        print("No employees found.")
        return

    table = Texttable()
    table.header(["ID", "Name", "Department"])
    for employee in employees:
        table.add_row([employee.id, employee.name, employee.department.name])
    
    print(table.draw())
