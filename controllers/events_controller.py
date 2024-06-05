from models.events import Event
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config.settings import DATABASE_URL
from rich.console import Console
from rich.table import Table

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
    console = Console()
    events = session.query(Event).all()

    if not events:
        print("No events found.")
        return
    
    table = Table(title="List of all events", show_header=True, header_style="magenta", show_lines=True)
    table.add_column("ID", justify="center")
    table.add_column("Name", justify="center")
    table.add_column("Start Date", justify="center")
    table.add_column("End Date", justify="center")
    table.add_column("Location", justify="center")
    table.add_column("Attendees", justify="center")
    table.add_column("Notes", justify="center")
    table.add_column("Contract ID", justify="center")
    table.add_column("Customer name", justify="center")
    table.add_column("Employee contact", justify="center")

    for event in events:
        table.add_row(str(event.id), event.name, str(event.start_date), str(event.end_date), event.location,
                       str(event.attendees), event.notes, str(event.contract_id), event.customer.fullname, event.employee.name)
    
    console.print(table)

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
