from controllers.contracts_controller import get_contracts, create_contract, update_contract
from controllers.customers_controller import get_customers
from controllers.employees_controller import get_employees
from models.contracts import Contract
from models.customers import Customer
from models.employees import Employee
from config.settings import DATABASE_URL
from config.helper_functions import get_valid_int, get_valid_id, get_valid_float
from sqlalchemy.orm import sessionmaker
from rich.console import Console
from rich.table import Table
from sqlalchemy import create_engine
from config.auth import get_logged_in_user
from config.decorators import permission_required
import config.session_manager as session_manager

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def manage_contracts_menu():
    """
    Main menu for contracts.
    Possibility to choose to create, read, update all the contracts.
    """
    console = Console()

    while True:
        table = Table(show_header=True, header_style="bold green")
        table.add_column("Contracts menu, please select an option: ", justify="left", style="cyan")

        table.add_row("1. Create a new contract")
        table.add_row("2. Show all the contracts")
        table.add_row("3. Update a contract")
        table.add_row("4. Go back")

        console.print(table)

        choice = input("Enter your choice: ")

        if choice == '1':
            create_contract_view()
        elif choice == '2':
            get_contracts(session)
        elif choice == '3':
            update_contract_view()
        elif choice == '4':
            break
        else:
            console.print("\nInvalid choice, try again\n", style="bold red")


@permission_required('create_contracts')
def create_contract_view():
    """
    Display a form to create a new contract and save it to the database.

    This function prompts the user to input the necessary information to create a new contract,
    including total price, pending amount, customer ID, and employee ID. It then calls the
    create_contract function to save the new contract to the database.

    Permissions:
        Requires 'create_contracts' permission.

    Inputs:
        total_price (float): The total price of the contract.
        pending_amount (float): The pending amount of the contract.
        customer_id (int): The ID of the customer associated with the contract.
        employee_id (int): The ID of the employee associated with the contract.

    Outputs:
        str: Result message indicating the success or failure of the contract creation.
    """
    console = Console()
    user, _ = get_logged_in_user(session_manager.get_current_token())
    if not user:
        console.print("Please login.", style="bold red")
        return

    total_price = get_valid_float("Enter total price of the contract: ")
    pending_amount = get_valid_float("Enter pending amount: ")
    customer_id = get_valid_id(session, "Enter the customer ID associated to that contract: ",
                               get_customers, Customer, allow_blank=False)
    employee_id = get_valid_id(session, "Enter the employee ID associated to that contract: ",
                               get_employees, Employee, allow_blank=False)

    result = create_contract(session, total_price, pending_amount, customer_id, employee_id)
    if result == "Contract created successfully!":
        console.print(result, style="bold green")
    else:
        console.print(result, style="bold red")


@permission_required('update_contracts')
def update_contract_view():
    """
    Display a form to update an existing contract and save the changes to the database.

    This function lists the current contracts and prompts the user to select a contract to update.
    It then prompts the user to input new values for the total price, pending amount, and signed status,
    and calls the update_contract function to save the changes to the database.

    Permissions:
        Requires 'update_contracts' permission.

    Inputs:
        contract_id (int): The ID of the contract to update.
        total_price (float): The new total price of the contract (optional).
        pending_amount (float): The new pending amount of the contract (optional).
        is_signed (bool): The new signed status of the contract (optional).

    Outputs:
        str: Result message indicating the success or failure of the contract update.
    """
    console = Console()
    user, _ = get_logged_in_user(session_manager.get_current_token())
    if not user:
        console.print("Please login.", style="bold red")
        return

    while True:
        print("Choose the contract to update:")
        get_contracts(session)

        contract_id = get_valid_int("Enter the contract ID to update: ")
        contract = session.query(Contract).get(contract_id)
        if not contract:
            console.print("Contract ID not found. Please choose an existing ID from the list.", style="bold red")
            continue

        total_price = get_valid_float("Enter new total price (leave blank to keep current): ", allow_blank=True)
        pending_amount = get_valid_float("Enter new pending amount (leave blank to keep current): ", allow_blank=True)
        is_signed = input("Is the contract signed ? (yes/no, leave blank to keep current): ")

        customer_id = get_valid_id(session, "Enter new customer ID (leave blank to keep current): ", get_customers,
                                   Customer, allow_blank=True, current_id=contract.customer_id)
        employee_id = get_valid_id(session, "Enter new employee ID (leave blank to keep current): ", get_employees,
                                   Employee, allow_blank=True, current_id=contract.employee_id)

        total_price = float(total_price) if total_price else None
        pending_amount = float(pending_amount) if pending_amount else None
        is_signed = True if is_signed.lower() == 'yes' else False if is_signed.lower() == 'no' else None
        customer_id = int(customer_id) if customer_id else None
        employee_id = int(employee_id) if employee_id else None

        result = update_contract(session, contract_id, total_price, pending_amount, is_signed,
                                 customer_id, employee_id)
        if result == "Contract updated successfully!":
            console.print(result, style="bold green")
        else:
            console.print(result, style="bold red")
        break
