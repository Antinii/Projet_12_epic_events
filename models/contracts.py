from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from .base import Base


class Contract(Base):
    __tablename__ = 'contracts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    total_price = Column(Float)
    pending_amount = Column(Float)
    created_date = Column(DateTime)
    is_signed = Column(Boolean, default=False)

    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship("Customer", back_populates="contracts")

    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship("Employee", back_populates="contracts")
