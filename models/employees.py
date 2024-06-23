from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import Base
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


class Employee(Base):
    """
    SQLAlchemy model for representing employees.

    This class defines a SQLAlchemy model for storing employee details such as name, hashed password,
    department affiliation, and relationships with customers, contracts, events, and departments.

    Attributes:
        id (int): Primary key identifier for the employee.
        name (str): Unique name of the employee.
        password (str): Hashed password using Argon2.

    Relationships:
        department_id (int): Foreign key referencing the ID of the department to which the employee belongs.
        department (relationship): Relationship to the Department entity, representing the department to which
        the employee belongs.
        customer (relationship): Relationship to the Customer entity, representing customers associated with the
        employee as a contact person.
        contract (relationship): Relationship to the Contract entity, representing contracts associated with the
        employee.
        event (relationship): Relationship to the Event entity, representing events associated with the employee.

    Methods:
        set_password(password):
            Hashes the provided password using Argon2 and sets it as the employee's password.

        check_password(password):
            Verifies the provided password against the hashed password using Argon2.

        get_permissions():
            Retrieves the permissions associated with the employee's department.
    """
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)
    password = Column(String(100))

    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship("Department", back_populates="employees")

    customer = relationship("Customer", back_populates="contact")
    contract = relationship("Contract", back_populates="employee")
    event = relationship("Event", back_populates="employee")

    def set_password(self, password):
        self.password = ph.hash(password)

    def check_password(self, password):
        try:
            return ph.verify(self.password, password)
        except VerifyMismatchError:
            return False

    def get_permissions(self):
        from config.permissions import PERMISSIONS
        return PERMISSIONS.get(self.department.name, [])
