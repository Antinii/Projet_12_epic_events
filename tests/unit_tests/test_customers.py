from datetime import datetime, timezone
from models.customers import Customer
from models.employees import Employee
from controllers.customers_controller import create_customer, update_customer, get_customers


def test_customer_model_creation(session):
    new_customer = Customer(
        fullname="Test Customer",
        email="test@customer.com",
        phone="123456789",
        company_name="Test Company",
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc),
        contact_id=1
    )
    session.add(new_customer)
    session.commit()
    assert new_customer.id is not None
    assert new_customer.fullname == "Test Customer"
    assert new_customer.email == "test@customer.com"
    assert new_customer.phone == "123456789"
    assert new_customer.company_name == "Test Company"


def test_create_customer_success(session):
    result = create_customer(session, "Test Customer", "test@customer.com", "123456789", "Test Company", 1)
    assert result == "Customer created successfully!"
    customer = session.query(Customer).filter_by(email="test@customer.com").first()
    assert customer is not None
    assert customer.fullname == "Test Customer"


def test_create_customer_duplicate_email(session):
    create_customer(session, "Test Customer", "test@customer.com", "123456789", "Test Company", 1)
    result = create_customer(session, "Another Customer", "test@customer.com", "987654321", "Another Company", 2)
    assert result == "This customer already exists, please choose another email."


def test_update_customer_success(session):
    create_customer(session, "Update Customer", "update@customer.com", "123456789", "Update Company", 1)
    customer = session.query(Customer).filter_by(email="update@customer.com").first()
    result = update_customer(session, customer.id, fullname="Updated Name")
    assert result == "Customer updated successfully!"
    assert customer.fullname == "Updated Name"

    result = update_customer(session, customer.id, email="newupdate@customer.com")
    assert result == "Customer updated successfully!"
    assert customer.email == "newupdate@customer.com"

    result = update_customer(session, customer.id, phone="987654321")
    assert result == "Customer updated successfully!"
    assert customer.phone == "987654321"

    result = update_customer(session, customer.id, company_name="New Company")
    assert result == "Customer updated successfully!"
    assert customer.company_name == "New Company"


def test_update_customer_not_found(session):
    result = update_customer(session, 999, fullname="Non-existent Customer")
    assert result == "Customer not found."


def test_get_customers(session, capsys):
    employee = Employee(name="Test Employee", password="password")
    session.add(employee)
    session.commit()

    create_customer(session, "Customer One", "one@customer.com", "111111111", "Company One", employee.id)
    create_customer(session, "Customer Two", "two@customer.com", "222222222", "Company Two", employee.id)

    get_customers(session)
    captured = capsys.readouterr()

    print("Captured Output:\n", captured.out)

    assert "One" in captured.out
    assert "Two" in captured.out
