from settings import DATABASE_URL
from models.customers import Customer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from texttable import Texttable
from datetime import datetime

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def get_customers():
    """
    Show all customers in a nice table format.
    """
    customers = session.query(Customer).all()

    if not customers:
        print("No customers found.")
        return

    table = Texttable()
    table.header(["ID", "Full Name", "Email", "Phone", "Company Name", "Created Date", "Updated Date", "Contact"])
    for customer in customers:
        table.add_row([customer.id, customer.fullname, customer.email, customer.phone, customer.company_name,
                       customer.created_date, customer.updated_date, customer.contact.name])
    
    print(table.draw())

def create_customer(fullname, email, phone, company_name, contact_id):
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
