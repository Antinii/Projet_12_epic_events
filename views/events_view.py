from controllers.events_controller import get_events, create_event, update_event
from controllers.customers_controller import get_customers
from controllers.contracts_controller import get_contracts
from controllers.employees_controller import get_employees
from models.contracts import Contract
from models.customers import Customer
from models.employees import Employee
from models.events import Event
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config.helper_functions import get_valid_date, get_valid_int, get_valid_id
from config.settings import DATABASE_URL
from config.auth import get_logged_in_user
from config.decorators import permission_required
from rich.console import Console
from rich.table import Table
import config.session_manager as session_manager

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def manage_events_menu():
    """
    Display for events menu.
    """
    console = Console()

    while True:
        table = Table(show_header=True, header_style="bold green")
        table.add_column("Events menu, please select an option", justify="left", style="cyan")

        table.add_row("1. Create a new event")
        table.add_row("2. Show all the events")
        table.add_row("3. Update an event")
        table.add_row("4. Go back")

        console.print(table)

        choice = input("Enter your choice: ")

        if choice == '1':
            create_event_view()
        elif choice == '2':
            get_events(session)
        elif choice == '3':
            update_event_view()
        elif choice == '4':
            break
        else:
            console.print("\nInvalid choice, try again\n", style="bold red")


@permission_required('create_events')
def create_event_view():
    """
    Display a form to create a new event and save it to the database.

    This function prompts the user to input the details for a new event, including the event name,
    start and end dates, location, number of attendees, notes, contract ID, customer ID, and employee ID.
    It calls the create_event function to save the new event to the database.

    Permissions:
        Requires 'create_events' permission.

    Inputs:
        name (str): The name of the event.
        start_date (str): The start date of the event in YYYY-MM-DD format.
        end_date (str): The end date of the event in YYYY-MM-DD format.
        location (str): The location of the event.
        attendees (int): The number of attendees for the event.
        notes (str): Additional notes for the event.
        contract_id (int): The ID of the related contract.
        customer_id (int): The ID of the related customer.
        employee_id (int): The ID of the employee creating the event.

    Outputs:
        str: Result message indicating the success or failure of the event creation.
    """
    console = Console()
    user, _ = get_logged_in_user(session_manager.get_current_token())

    name = input("Enter the name of the event: ")

    start_date = get_valid_date("Enter start date (YYYY-MM-DD): ", allow_blank=False)
    end_date = get_valid_date("Enter end date (YYYY-MM-DD): ", allow_blank=False)

    location = input("Enter the location of the event: ")
    attendees = get_valid_int("Enter the number of attendees: ")
    notes = input("Enter notes: ")
    contract_id = get_valid_id(session, "Enter contract ID: ", get_contracts, Contract, allow_blank=False)
    customer_id = get_valid_id(session, "Enter customer ID: ", get_customers, Customer, allow_blank=False)
    employee_id = user.id

    result = create_event(session, name, start_date, end_date, location, attendees,
                          notes, contract_id, customer_id, employee_id)
    if result == "Event created successfully!":
        console.print(result, style="bold green")
    else:
        console.print(result, style="bold red")


@permission_required('update_events')
def update_event_view():
    """
    Display a form to update an existing event and save the changes to the database.

    This function lists the current events and prompts the user to select an event to update.
    It then prompts the user to input new values for the event details, such as name, start date, end date,
    location, number of attendees, notes, contract ID, customer ID, and employee ID. The function then calls
    update_event to save the changes to the database.

    Permissions:
        Requires 'update_events' permission.

    Inputs:
        event_id (int): The ID of the event to update.
        name (str): The new name of the event (optional).
        start_date (str): The new start date of the event in YYYY-MM-DD format (optional).
        end_date (str): The new end date of the event in YYYY-MM-DD format (optional).
        location (str): The new location of the event (optional).
        attendees (int): The new number of attendees for the event (optional).
        notes (str): The new notes for the event (optional).
        contract_id (int): The new ID of the related contract (optional).
        customer_id (int): The new ID of the related customer (optional).
        employee_id (int): The new ID of the related employee (optional).

    Outputs:
        str: Result message indicating the success or failure of the event update.
    """
    console = Console()
    user, _ = get_logged_in_user(session_manager.get_current_token())
    if not user:
        console.print("Please login", style="bold red")
        return

    while True:
        print("Choose the event to update:")
        get_events(session)

        event_id = get_valid_int("Enter the event ID to update:")
        event = session.query(Event).get(event_id)
        if not event:
            console.print("Event ID not found. Please choose an existing ID from the list.", style="bold red")
            continue

        name = input("Enter the new name of the event (leave blank to keep current): ")

        start_date = get_valid_date("Enter new start date (YYYY-MM-DD, leave blank to keep current): ",
                                    allow_blank=True)
        end_date = get_valid_date("Enter new end date (YYYY-MM-DD, leave blank to keep current): ", allow_blank=True)

        location = input("Enter new location (leave blank to keep current): ")
        attendees = get_valid_int("Enter new number of attendees (leave blank to keep current): ", allow_blank=True)
        notes = input("Enter new notes (leave blank to keep current): ")

        contract_id = get_valid_id(session, "Enter new contract ID (leave blank to keep current): ", get_contracts,
                                   Contract, allow_blank=True, current_id=event.contract_id)
        customer_id = get_valid_id(session, "Enter new customer ID (leave blank to keep current): ", get_customers,
                                   Customer, allow_blank=True, current_id=event.customer_id)
        employee_id = get_valid_id(session, "Enter new employee ID (leave blank to keep current): ", get_employees,
                                   Employee, allow_blank=True, current_id=event.employee_id)

        start_date = start_date if start_date else None
        end_date = end_date if end_date else None
        location = location if location else None
        attendees = int(attendees) if attendees else None
        notes = notes if notes else None
        contract_id = int(contract_id) if contract_id else None
        customer_id = int(customer_id) if customer_id else None
        employee_id = int(employee_id) if employee_id else None

        result = update_event(
            session,
            event_id,
            name,
            start_date,
            end_date,
            location,
            attendees,
            notes,
            contract_id,
            customer_id,
            employee_id
        )
        if result == "Event updated successfully!":
            console.print(result, style="bold green")
        else:
            console.print(result, style="bold red")
        break
