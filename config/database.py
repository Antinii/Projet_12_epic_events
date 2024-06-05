from config.settings import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.contracts import Contract
from models.customers import Customer
from models.departments import Department
from models.employees import Employee
from models.events import Event

# Create an engine
engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
session.close()
