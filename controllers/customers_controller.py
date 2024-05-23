from models.customers import Customer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from texttable import Texttable

engine = create_engine('sqlite:///db.sqlite3')
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
    table.header(["ID", "Full Name", "Email", "Phone", "Company Name", "Created Date", "Updated Date"])
    for customer in customers:
        table.add_row([customer.id, customer.fullname, customer.email, customer.phone, customer.company_name,
                       customer.created_date, customer.updated_date])
    
    print(table.draw())