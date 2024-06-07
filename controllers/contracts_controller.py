from config.settings import DATABASE_URL
from models.contracts import Contract
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from rich.console import Console
from rich.table import Table
from datetime import datetime
from sentry_sdk import capture_message, capture_exception

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def get_contracts():
    """
    Show all contracts in a nice table format.
    """
    console = Console()
    contracts = session.query(Contract).all()

    if not contracts:
        print("No contracts found.")
        return

    table = Table(title="list of all the contracts", show_header=True, header_style="magenta", show_lines=True)

    table.add_column("ID", justify="center")
    table.add_column("Total Price", justify="center")
    table.add_column("Pending Amount", justify="center")
    table.add_column("Created Date", justify="center")
    table.add_column("Is Signed", justify="center")
    table.add_column("Customer", justify="center")
    table.add_column("Contact", justify="center")

    for contract in contracts:
        table.add_row(str(contract.id), str(contract.total_price), str(contract.pending_amount), str(contract.created_date),
                       str(contract.is_signed), contract.customer.fullname, contract.employee.name)
    
    console.print(table)

def create_contract(total_price, pending_amount, customer_id, employee_id):
    """
    Create a contract in the database
    """
    new_contract = Contract(
        total_price=total_price,
        pending_amount=pending_amount,
        created_date=datetime.utcnow(),
        is_signed=False,
        customer_id=customer_id,
        employee_id=employee_id
    )
    session.add(new_contract)
    session.commit()
    return "Contract created successfully!"

def update_contract(contract_id, total_price=None, pending_amount=None,
                    is_signed=None, customer_id=None, employee_id=None):
    """
    Update an existing contract in the database.
    """
    try:
        contract = session.query(Contract).get(contract_id)
        if not contract:
            return "Contract not found."
        if total_price is not None:
            contract.total_price = total_price
        if pending_amount is not None:
            contract.pending_amount = pending_amount
        if is_signed is not None:
            contract.is_signed = is_signed
            if is_signed:
                capture_message(f"Contract {contract_id} is signed !", level="info")
        if customer_id is not None:
            contract.customer_id = customer_id
        if employee_id is not None:
            contract.employee_id = employee_id
        session.commit()
        return "Contract updated successfully!"
    except Exception as e:
        session.rollback()
        capture_exception(e)
        return "Error updating contract."
