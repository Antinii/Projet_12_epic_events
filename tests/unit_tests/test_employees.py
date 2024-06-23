from models.employees import Employee
from controllers.employees_controller import create_employee, login_employee, update_employee, delete_employee


def test_set_password(session):
    employee = Employee(name="test_user")
    employee.set_password("password")
    assert employee.password is not None
    assert employee.password != "password"


def test_check_password(session):
    employee = Employee(name="test_user")
    employee.set_password("password")
    assert employee.check_password("password")
    assert not employee.check_password("wrong_password")


def test_create_employee_with_whitespace(session):
    result = create_employee(session, "   ", "password", 1)
    assert result == "Name and password cannot be empty."

    result = create_employee(session, "name", "   ", 1)
    assert result == "Name and password cannot be empty."

    result = create_employee(session, "   ", "   ", 1)
    assert result == "Name and password cannot be empty."


def test_create_employee_success(session):
    result = create_employee(session, "test_user", "password", 1)
    assert result == "User created successfully!"
    employee = session.query(Employee).filter_by(name="test_user").first()
    assert employee is not None


def test_login_employee_with_whitespace(session):
    create_employee(session, "test_user", "password", 1)

    result = login_employee(session, "   ", "password")
    assert result["message"] == "\n Username does not exist, please try again. \n"

    result = login_employee(session, "test_user", "   ")
    assert result["message"] == "\n Incorrect password, please try again. \n"


def test_login_employee_success(session):
    create_employee(session, "login_user", "password", 1)

    result = login_employee(session, "login_user", "password")
    assert result["message"] == "Login successful"


def test_update_employee_success(session):
    create_employee(session, "update_user_success", "password", 1)
    employee = session.query(Employee).filter_by(name="update_user_success").first()

    result = update_employee(session, employee.id, name="new_name")
    assert result == "Employee updated successfully!"
    assert employee.name == "new_name"

    result = update_employee(session, employee.id, password="new_password")
    assert result == "Employee updated successfully!"
    assert employee.check_password("new_password")


def test_delete_employee_success(session):
    create_employee(session, "delete_user", "password", 1)
    employee = session.query(Employee).filter_by(name="delete_user").first()
    result = delete_employee(session, employee.id)
    assert result == "Employee deleted successfully!"
    assert session.query(Employee).filter_by(name="delete_user").first() is None


def test_delete_employee_not_found(session):
    result = delete_employee(session, 999)
    assert result == "Employee not found."
