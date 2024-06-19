from config.settings import DATABASE_URL
from models.customers import Customer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from rich.console import Console
from rich.table import Table
from datetime import datetime

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def get_customers():
    """
    Show all customers in a nice table format.
    """
    console = Console()
    customers = session.query(Customer).all()

    if not customers:
        print("No customers found.")
        return

    table = Table(title="list of all the customers", show_header=True, header_style="magenta", show_lines=True)

    table.add_column("ID", justify="center")
    table.add_column("Full Name", justify="center")
    table.add_column("Email", justify="center")
    table.add_column("Phone", justify="center")
    table.add_column("Company Name", justify="center")
    table.add_column("Created Date", justify="center")
    table.add_column("Updated Date", justify="center")
    table.add_column("Contact", justify="center")

    for customer in customers:
        table.add_row(str(customer.id), customer.fullname, customer.email, customer.phone, customer.company_name,
                       str(customer.created_date), str(customer.updated_date), customer.contact.name)
    
    console.print(table)

def create_customer(fullname, email, phone, company_name, contact_id):
    """
    Create a customer and write it in the database.
    """
    if session.query(Customer).filter_by(email=email).first():
        return "This customer already exists, please choose another email."
    
    new_customer = Customer(
        fullname=fullname,
        email=email,
        phone=phone,
        company_name=company_name,
        contact_id=contact_id,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    session.add(new_customer)
    session.commit()
    return "Customer created successfully!"

def update_customer(customer_id, fullname=None, email=None, phone=None, company_name=None):
    """
    Update a customer already existing in the database.
    """
    customer = session.query(Customer).get(customer_id)
    if not customer:
        return "Customer not found."
    if fullname:
        customer.fullname = fullname
    if email:
        customer.email = email
    if phone:
        customer.phone = phone
    if company_name:
        customer.company_name = company_name
    customer.updated_date = datetime.utcnow()
    session.commit()
    return "Customer updated successfully!"
