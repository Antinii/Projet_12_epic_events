from datetime import datetime, timezone
from models.contracts import Contract
from models.customers import Customer
from models.employees import Employee
from controllers.contracts_controller import create_contract, update_contract, get_contracts


def test_contract_model_creation(session):
    new_contract = Contract(
        total_price=1000.0,
        pending_amount=500.0,
        created_date=datetime.now(timezone.utc),
        is_signed=False,
        customer_id=1,
        employee_id=1
    )
    session.add(new_contract)
    session.commit()
    assert new_contract.id is not None
    assert new_contract.total_price == 1000.0
    assert new_contract.pending_amount == 500.0
    assert new_contract.is_signed is False


def test_create_contract_success(session):
    customer = Customer(fullname="Test Customer", email="test@customer.com",
                        phone="123456789", company_name="Test Company")
    session.add(customer)
    employee = Employee(name="Test Employee", password="password")
    session.add(employee)
    session.commit()

    result = create_contract(session, 1000.0, 500.0, customer.id, employee.id)
    assert result == "Contract created successfully!"
    contract = session.query(Contract).filter_by(customer_id=customer.id, employee_id=employee.id).first()
    assert contract is not None
    assert contract.total_price == 1000.0
    assert contract.pending_amount == 500.0


def test_update_contract_success(session):
    customer = Customer(fullname="Test Customer", email="test@customer.com",
                        phone="123456789", company_name="Test Company")
    session.add(customer)
    employee = Employee(name="Test Employee", password="password")
    session.add(employee)
    session.commit()

    create_contract(session, 1000.0, 500.0, customer.id, employee.id)
    contract = session.query(Contract).filter_by(customer_id=customer.id, employee_id=employee.id).first()

    result = update_contract(session, contract.id, total_price=1500.0, pending_amount=300.0, is_signed=True)
    assert result == "Contract updated successfully!"
    assert contract.total_price == 1500.0
    assert contract.pending_amount == 300.0
    assert contract.is_signed is True


def test_update_contract_not_found(session):
    result = update_contract(session, 999, total_price=1500.0)
    assert result == "Contract not found."


def test_get_contracts(session, capsys):
    customer = Customer(fullname="Test Customer", email="test@customer.com",
                        phone="123456789", company_name="Test Company")
    session.add(customer)
    employee = Employee(name="Test Employee", password="password")
    session.add(employee)
    session.commit()

    create_contract(session, 1000.0, 500.0, customer.id, employee.id)
    create_contract(session, 2000.0, 1500.0, customer.id, employee.id)

    get_contracts(session)
    captured = capsys.readouterr()
    assert "1000.0" in captured.out
    assert "2000.0" in captured.out
