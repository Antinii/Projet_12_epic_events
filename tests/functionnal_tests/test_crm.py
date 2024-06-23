import pytest
from models.customers import Customer
from models.base import Base
from controllers.employees_controller import create_employee, login_employee
from controllers.customers_controller import create_customer, get_customers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import TEST_DATABASE_URL
import config.session_manager as session_manager

engine = create_engine(TEST_DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


@pytest.fixture(scope='module')
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_crm_functionality(setup_database):
    # Step 1: Create an employee
    result = create_employee(session, "Test Employee", "password", 1)
    assert result == "User created successfully!"

    # Step 2: Log in with the created employee
    login_result = login_employee(session, "Test Employee", "password")
    assert login_result["message"] == "Login successful"
    session_manager.set_current_token(login_result["token"])

    # Step 3: Create a customer
    result = create_customer(session, "Customer One", "one@customer.com", "111111111", "Company One", 1)
    assert result == "Customer created successfully!"

    # Step 4: Fetch and verify the list of customers
    customers = session.query(Customer).all()
    assert len(customers) == 1
    assert customers[0].fullname == "Customer One"
    assert customers[0].email == "one@customer.com"
    assert customers[0].phone == "111111111"
    assert customers[0].company_name == "Company One"

    # Print the customers to verify the output
    get_customers(session)
