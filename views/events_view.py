from texttable import Texttable
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
from settings import DATABASE_URL
from auth import get_logged_in_user
from decorators import permission_required
from datetime import datetime
import session_manager

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def manage_events_menu():
    while True:
        table = Texttable()
        table.header(["Events menu, please select an option"])
        table.add_row(["1. Create a new event"])
        table.add_row(["2. Show all the events"])
        table.add_row(["3. Update an event"])
        table.add_row(["4. Go back"])
        print(table.draw())

        choice = input("Enter your choice: ")

        if choice == '1':
            create_event_view()
        elif choice == '2':
            get_events()
        elif choice == '3':
            update_event_view()
        elif choice == '4':
            break
        else:
            print("Invalid choice")


@permission_required('create_events')
def create_event_view():
    user = get_logged_in_user(session_manager.get_current_token())
    if not user:
        print("Please login.")
        return
    
    name = input("Enter the name of the event: ")

    while True:
        try:
            start_date = input("Enter start date (YYYY-MM-DD): ")
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    while True:
        try:
            end_date = input("Enter end date (YYYY-MM-DD): ")
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    location = input("Enter the location of the event: ")
    attendees = int(input("Enter the number of attendees: "))
    notes = input("Enter notes: ")
    get_contracts()
    contract_id = input("Select the contract ID: ")
    get_customers()
    customer_id = input("Select the customer ID: ")
    employee_id = user.id

    result = create_event(name, start_date, end_date, location, attendees, notes, contract_id, customer_id, employee_id)
    print(result)

@permission_required('update_events')
def update_event_view():
    user = get_logged_in_user(session_manager.get_current_token())
    if not user:
        print("Please login.")
        return
    
    while True:
        print("Choose the event to update:")
        get_events()

        event_id = (input("Enter the event ID to update:"))
        if not event_id.isdigit():
            print("Please enter a valid numeric ID.")
            continue

        event_id = int(event_id)
        event = session.query(Event).get(event_id)
        if not event:
            print("Event ID not found. Please choose an existing ID from the list.")
            continue

        name = input("Enter the new name of the event (leave blank to keep current): ")

        while True:
            try:
                start_date = input("Enter new start date (YYYY-MM-DD, leave blank to keep current): ")
                if start_date:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

        while True:
            try:
                end_date = input("Enter new end date (YYYY-MM-DD, leave blank to keep current): ")
                if end_date:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

        location = input("Enter new location (leave blank to keep current): ")
        attendees = input("Enter new number of attendees (leave blank to keep current): ")
        notes = input("Enter new notes (leave blank to keep current): ")

        while True:
            get_contracts()
            contract_id = input("Enter new contract ID (leave blank to keep current): ")
            if contract_id == "":
                contract_id = event.contract_id
                break
            if not contract_id.isdigit():
                print("Please enter a valid numeric ID.")
                continue
            contract_id = int(contract_id)
            contract = session.query(Contract).get(contract_id)
            if not contract:
                print("Contract ID not found. Please choose an existing ID from the list.")
                continue
            break
        
        while True:
            get_customers()
            customer_id = input("Enter new customer ID (leave blank to keep current): ")
            if customer_id == "":
                customer_id = event.customer_id
                break
            if not customer_id.isdigit():
                print("Please enter a valid numeric ID.")
                continue
            customer_id = int(customer_id)
            customer = session.query(Customer).get(customer_id)
            if not customer:
                print("Customer ID not found. Please choose an existing ID from the list.")
                continue
            break
        
        while True:       
            get_employees()
            employee_id = input("Enter new employee ID (leave blank to keep current): ")
            if employee_id == "":
                employee_id = event.employee_id
                break
            if not employee_id.isdigit():
                print("Please enter a valid numeric ID.")
                continue
            employee_id = int(employee_id)
            employee = session.query(Employee).get(employee_id)
            if not employee:
                print("Employee ID not found. Please choose an existing ID from the list.")
                continue
            break

        start_date = start_date if start_date else None
        end_date = end_date if end_date else None
        location = location if location else None
        attendees = int(attendees) if attendees else None
        notes = notes if notes else None
        contract_id = int(contract_id) if contract_id else None
        customer_id = int(customer_id) if customer_id else None
        employee_id = int(employee_id) if employee_id else None

        result = update_event(
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
        print(result)
        break
