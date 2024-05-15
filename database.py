from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.contracts import Contract
from models.customers import Customer
from models.departments import Department
from models.employees import Employee
from models.events import Event

# Define the path to your SQLite database file
DATABASE_URL = "sqlite:///db.sqlite3"

# Create an engine
engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(engine)

# Optional: If you need to interact with the database, create a session
Session = sessionmaker(bind=engine)
session = Session()

# Close the session when done
session.close()
