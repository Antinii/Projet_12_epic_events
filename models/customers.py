from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Customer(Base):
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
    