from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import Base


class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)
    password = Column(String(100))

    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship("Department", back_populates="employees")
