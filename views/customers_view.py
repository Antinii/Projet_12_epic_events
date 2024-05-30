from texttable import Texttable
from controllers.customers_controller import get_customers, create_customer, update_customer
from models.customers import Customer
from settings import DATABASE_URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from auth import get_logged_in_user
from decorators import permission_required
import session_manager

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def manage_customers_menu():
    while True:
        table = Texttable()
        table.header(["Customers menu, please select an option"])
        table.add_row(["1. Create a new customer"])
        table.add_row(["2. Show all the customers"])
        table.add_row(["3. Update a customer"])
        table.add_row(["4. Go back"])
        print(table.draw())

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
            print("Invalid choice")


@permission_required('create_customers')
def create_customer_view():
    """
    Create a new customer in the database.
    """
    user = get_logged_in_user(session_manager.get_current_token())
    if not user:
        print("Please login.")
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
    while True:
        print("Choose the customer to update:")
        get_customers()

        customer_id = input("Enter the customer ID to update: ")
        if not customer_id.isdigit():
            print("Please enter a valid numeric ID.")
            continue

        customer_id = int(customer_id)
        customer = session.query(Customer).get(customer_id)
        if not customer:
            print("Customer ID not found. Please choose an existing ID from the list.")
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