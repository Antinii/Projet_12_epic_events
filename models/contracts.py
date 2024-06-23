from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from .base import Base


class Contract(Base):
    """
    SQLAlchemy model for representing contracts.

    This class defines a SQLAlchemy model for storing contract details such as total price, pending amount,
    creation date, signature status, and relationships with customers, employees, and events.

    Attributes:
        id (int): Primary key identifier for the contract.
        total_price (float): Total price of the contract.
        pending_amount (float): Pending amount to be paid.
        created_date (datetime): Date and time when the contract was created.
        is_signed (bool): Boolean indicating if the contract has been signed (default is False).

    Relationships:
        customer_id (int): Foreign key referencing the ID of the customer associated with the contract.
        customer (relationship): Relationship to the Customer entity, representing the customer associated
        with the contract.
        employee_id (int): Foreign key referencing the ID of the employee responsible for the contract.
        employee (relationship): Relationship to the Employee entity, representing the employee responsible
        for the contract.
        event (relationship): Relationship to the Event entity, representing events associated with the contract.
    """
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_price = Column(Float)
    pending_amount = Column(Float)
    created_date = Column(DateTime)
    is_signed = Column(Boolean, default=False)

    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship("Customer", back_populates="contract")

    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship("Employee", back_populates="contract")

    event = relationship("Event", back_populates="contract")
