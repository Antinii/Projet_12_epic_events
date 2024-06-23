from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Customer(Base):
    """
    SQLAlchemy model for representing customers.

    This class defines a SQLAlchemy model for storing customer details such as full name, email, phone number,
    company name, and related entities like contacts (employees), contracts, and events.

    Attributes:
        id (int): Primary key identifier for the customer.
        fullname (str): Full name of the customer.
        email (str): Email address of the customer (unique).
        phone (str): Phone number of the customer.
        company_name (str): Name of the company associated with the customer.
        created_date (datetime): Date and time when the customer record was created.
        updated_date (datetime): Date and time when the customer record was last updated.

    Relationships:
        contact_id (int): Foreign key referencing the ID of the employee who is the contact person for the customer.
        contact (relationship): Relationship to the Employee entity, representing the contact person associated
        with the customer.
        contract (relationship): Relationship to the Contract entity, representing contracts associated with
        the customer.
        event (relationship): Relationship to the Event entity, representing events associated with the customer.
    """
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(100))
    email = Column(String(100), unique=True)
    phone = Column(String(30))
    company_name = Column(String(100))
    created_date = Column(DateTime)
    updated_date = Column(DateTime)

    contact_id = Column(Integer, ForeignKey('employees.id'))
    contact = relationship("Employee", back_populates="customer")

    contract = relationship("Contract", back_populates="customer")
    event = relationship("Event", back_populates="customer")
