from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Department(Base):
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    employees = relationship("Employee", back_populates="department")
