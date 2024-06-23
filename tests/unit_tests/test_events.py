from datetime import date
from models.events import Event
from models.customers import Customer
from models.contracts import Contract
from models.employees import Employee
from controllers.events_controller import create_event, update_event, get_events


def test_event_model_creation(session):
    new_event = Event(
        name="Test Event",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 2),
        location="Test Location",
        attendees=100,
        notes="Test Notes",
        contract_id=1,
        customer_id=1,
        employee_id=1
    )
    session.add(new_event)
    session.commit()
    assert new_event.id is not None
    assert new_event.name == "Test Event"
    assert new_event.location == "Test Location"
    assert new_event.attendees == 100
    assert new_event.notes == "Test Notes"


def test_create_event_success(session):
    customer = Customer(fullname="Test Customer", email="test@customer.com",
                        phone="123456789", company_name="Test Company")
    session.add(customer)
    employee = Employee(name="Test Employee", password="password")
    session.add(employee)
    contract = Contract(total_price=1000.0, pending_amount=500.0, customer_id=customer.id, employee_id=employee.id)
    session.add(contract)
    session.commit()

    result = create_event(session, "Test Event", date(2024, 1, 1), date(2024, 1, 2),
                          "Test Location", 100, "Test Notes", contract.id, customer.id, employee.id)
    assert result == "Event created successfully!"
    event = session.query(Event).filter_by(name="Test Event").first()
    assert event is not None
    assert event.location == "Test Location"
    assert event.attendees == 100
    assert event.notes == "Test Notes"


def test_update_event_success(session):
    customer = Customer(fullname="Test Customer", email="test@customer.com",
                        phone="123456789", company_name="Test Company")
    session.add(customer)
    employee = Employee(name="Test Employee", password="password")
    session.add(employee)
    contract = Contract(total_price=1000.0, pending_amount=500.0, customer_id=customer.id, employee_id=employee.id)
    session.add(contract)
    session.commit()

    create_event(session, "Test Event", date(2024, 1, 1), date(2024, 1, 2),
                 "Test Location", 100, "Test Notes", contract.id, customer.id, employee.id)
    event = session.query(Event).filter_by(name="Test Event").first()

    result = update_event(session, event.id, name="Updated Event", location="Updated Location", attendees=200)
    assert result == "Event updated successfully!"
    assert event.name == "Updated Event"
    assert event.location == "Updated Location"
    assert event.attendees == 200


def test_update_event_not_found(session):
    result = update_event(session, 999, name="Non-existent Event")
    assert result == "Event not found."


def test_get_events(session, capsys):
    customer = Customer(fullname="Test Customer", email="test@customer.com",
                        phone="123456789", company_name="Test Company")
    session.add(customer)
    employee = Employee(name="Test Employee", password="password")
    session.add(employee)
    contract = Contract(total_price=1000.0, pending_amount=500.0, customer_id=customer.id, employee_id=employee.id)
    session.add(contract)
    session.commit()

    create_event(session, "Event One", date(2024, 1, 1), date(2024, 1, 2),
                 "Location One", 100, "Notes One", contract.id, customer.id, employee.id)
    create_event(session, "Event Two", date(2024, 2, 1), date(2024, 2, 2),
                 "Location Two", 200, "Notes Two", contract.id, customer.id, employee.id)

    get_events(session)
    captured = capsys.readouterr()
    assert "One" in captured.out
    assert "Two" in captured.out
