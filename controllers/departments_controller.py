from config.settings import DATABASE_URL
from models.departments import Department
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def get_departments():
    """
    Fetch and return all departments from the database.

    Returns:
        list: List of all departments.
    """
    return session.query(Department).all()
