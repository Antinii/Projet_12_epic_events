from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from .base import Base


class Event(Base):
    """
    SQLAlchemy model for representing events.

    This class defines a SQLAlchemy model for storing event details such as event name, start and end dates,
    location, number of attendees, notes, and relationships with contracts, customers, and employees.

    Attributes:
        id (int): Primary key identifier for the event.
        name (str): Name or title of the event.
        start_date (datetime.date): Date when the event starts.
        end_date (datetime.date): Date when the event ends.
        location (str): Location or venue of the event.
        attendees (int): Number of attendees expected for the event.
        notes (str): Additional notes or description about the event.

    Relationships:
        contract_id (int): Foreign key referencing the ID of the contract associated with the event.
        contract (relationship): Relationship to the Contract entity, representing the contract associated
        with the event.
        customer_id (int): Foreign key referencing the ID of the customer associated with the event.
        customer (relationship): Relationship to the Customer entity, representing the customer associated
        with the event.
        employee_id (int): Foreign key referencing the ID of the employee responsible for the event.
        employee (relationship): Relationship to the Employee entity, representing the employee responsible
        for the event.
    """
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    location = Column(String(200))
    attendees = Column(Integer)
    notes = Column(Text)

    contract_id = Column(Integer, ForeignKey('contracts.id'))
    contract = relationship("Contract", back_populates="event")

    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship("Customer", back_populates="event")

    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship("Employee", back_populates="event")
