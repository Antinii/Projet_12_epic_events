from config.settings import DATABASE_URL
from models.departments import Department
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from rich.console import Console
from rich.table import Table

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def get_departments():
    """
    Fetch and return all departments from the database.

    Returns:
        list: List of all departments.
    """
    console = Console()
    departments = session.query(Department).all()

    if not departments:
        print("No departments found.")
        return
    
    table = Table(title="List of all Departments", show_header=True, header_style="magenta", show_lines=True)

    table.add_column("ID", justify="center")
    table.add_column("Department Name", justify="left")

    for dept in departments:
        table.add_row(str(dept.id), dept.name)

    console.print(table)
