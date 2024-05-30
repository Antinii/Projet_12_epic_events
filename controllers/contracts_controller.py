from settings import DATABASE_URL
from models.contracts import Contract
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from texttable import Texttable
from datetime import datetime

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def get_contracts():
    """
    Show all contracts in a nice table format.
    """
    contracts = session.query(Contract).all()

    if not contracts:
        print("No contracts found.")
        return

    table = Texttable()
    table.header(["ID", "Total Price", "Pending Amount", "Created Date", "Is Signed", "Customer", "Contact"])
    for contract in contracts:
        table.add_row([contract.id, contract.total_price, contract.pending_amount, contract.created_date,
                       contract.is_signed, contract.customer.fullname, contract.employee.name])
    
    print(table.draw())

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
    contract = session.query(Contract).get(contract_id)
    if not contract:
        return "Contract not found."
    if total_price is not None:
        contract.total_price = total_price
    if pending_amount is not None:
        contract.pending_amount = pending_amount
    if is_signed is not None:
        contract.is_signed = is_signed
    if customer_id is not None:
        contract.customer_id = customer_id
    if employee_id is not None:
        contract.employee_id = employee_id
    session.commit()
    return "Contract updated successfully!"
