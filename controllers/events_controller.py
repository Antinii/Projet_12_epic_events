from models.events import Event
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from settings import DATABASE_URL
from texttable import Texttable

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def create_event(name, start_date, end_date, location, attendees, notes, contract_id, customer_id, employee_id):
    """
    Function creating an event in the database.
    """
    new_event = Event(
        name=name,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        contract_id=contract_id,
        customer_id=customer_id,
        employee_id=employee_id
    )
    session.add(new_event)
    session.commit()
    return "Event created successfully!"

def get_events():
    """
    Show all events in a nice table format.
    """
    events = session.query(Event).all()

    if not events:
        print("No events found.")
        return
    
    table = Texttable()
    table.header(["ID", "Name", "Start Date", "End Date", "Location", "Attendees",
                  "Notes", "Contract ID", "Customer name", "Employee contact"])
    for event in events:
        table.add_row([event.id, event.name, event.start_date, event.end_date, event.location,
                       event.attendees, event.notes, event.contract_id, event.customer.fullname, event.employee.name])
    
    print(table.draw())

def update_event(event_id, name=None, start_date=None, end_date=None, location=None,
                 attendees=None, notes=None, contract_id=None, customer_id=None, employee_id=None):
    """
    Update an existing event in the database.
    """
    event = session.query(Event).get(event_id)
    if not event:
        return "Event not found."
    if name is not None:
        event.name = name
    if start_date is not None:
        event.start_date = start_date
    if end_date is not None:
        event.end_date = end_date
    if location is not None:
        event.location = location
    if attendees is not None:
        event.attendees = attendees
    if notes is not None:
        event.notes = notes
    if contract_id is not None:
        event.contract_id = contract_id
    if customer_id is not None:
        event.customer_id = customer_id
    if employee_id is not None:
        event.employee_id = employee_id
    session.commit()
    return "Event updated successfully!"
