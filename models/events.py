from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    location = Column(String(200))
    attendees = Column(Integer)
    notes = Column(Text)
    
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    contract = relationship("Contract", back_populates="events")
    
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship("Customer", back_populates="events")
    
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship("Employee", back_populates="events")
