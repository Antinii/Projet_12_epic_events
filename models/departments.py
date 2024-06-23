from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Department(Base):
    """
    SQLAlchemy model for representing departments.

    This class defines a SQLAlchemy model for storing department details such as department name and
    relationships with employees.

    Attributes:
        id (int): Primary key identifier for the department.
        name (str): Name of the department.

    Relationships:
        employees (relationship): Relationship to the Employee entity, representing employees belonging
        to this department.
    """
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    employees = relationship("Employee", back_populates="department")
