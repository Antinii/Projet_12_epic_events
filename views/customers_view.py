from controllers.customers_controller import get_customers, create_customer, update_customer
from models.customers import Customer
from config.settings import DATABASE_URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config.auth import get_logged_in_user
from config.decorators import permission_required
import config.session_manager as session_manager
from rich.console import Console
from rich.table import Table

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def manage_customers_menu():
    """
    Menu for customers
    """
    console = Console()

    while True:
        table = Table(show_header=True, header_style="bold green")
        table.add_column("Customers menu, please select an option: ", justify="left", style="cyan")
        
        table.add_row("1. Create a new customer")
        table.add_row("2. Show all the customers")
        table.add_row("3. Update a customer")
        table.add_row("4. Go back")
        
        console.print(table)

        choice = input("Enter your choice: ")

        if choice == '1':
            create_customer_view()
        elif choice == '2':
            get_customers()
        elif choice == '3':
            update_customer_view()
        elif choice == '4':
            break
        else:
            console.print("\nInvalid choice, try again\n", style="bold red")


@permission_required('create_customers')
def create_customer_view():
    """
    Create a new customer in the database.
    """
    console = Console()
    user = get_logged_in_user(session_manager.get_current_token())
    if not user:
        console.print("Please login.", style="bold red")
        return

    fullname = input("Enter the full name of the customer: ")
    email = input("Enter the email of the customer: ")
    phone = input("Enter the phone number of the customer: ")
    company_name = input("Enter the customer company name: ")
    contact_id = user.id

    result = create_customer(fullname, email, phone, company_name, contact_id)
    print(result)

@permission_required('update_customers')
def update_customer_view():
    """
    Display a form to update an existing customer and save the changes to the database.

    This function lists the current customers and prompts the user to select a customer to update. 
    It then prompts the user to input new values for the fullname, email, phone and company name, 
    and calls the update_customer function to save the changes to the database.

    Permissions:
        Requires 'update_customers' permission.

    Inputs:
        customer_id (int): The ID of the customer to update.
        fullname (str) : The new fullname of the customer (optional).
        email (str): The new mail of the customer (optional).
        phone (str): The new phone number of the customer (optional).
        company_name (str): The new company name of the customer (optional).

    Outputs:
        str: Result message indicating the success or failure of the customer update.
    """
    console = Console()
    while True:
        print("Choose the customer to update:")
        get_customers()

        customer_id = input("Enter the customer ID to update: ")
        if not customer_id.isdigit():
            console.print("Please enter a valid numeric ID.", style="bold red")
            continue

        customer_id = int(customer_id)
        customer = session.query(Customer).get(customer_id)
        if not customer:
            console.print("Customer ID not found. Please choose an existing ID from the list.", style="bold red")
            continue

        fullname = input("Enter new full name (leave blank to keep current): ")
        email = input("Enter new email (leave blank to keep current): ")
        phone = input("Enter new phone number (leave blank to keep current): ")
        company_name = input("Enter new company name (leave blank to keep current): ")

        result = update_customer(customer_id, 
                                fullname if fullname else None, 
                                email if email else None, 
                                phone if phone else None, 
                                company_name if company_name else None)
        print(result)
        break