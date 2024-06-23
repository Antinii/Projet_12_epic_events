import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import TEST_DATABASE_URL
from models.base import Base
from models.customers import Customer
from models.employees import Employee
from models.contracts import Contract
from models.events import Event
from models.departments import Department


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(TEST_DATABASE_URL)
    return engine


@pytest.fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope='function', autouse=True)
def clean_db(session):
    # Clean the database before each test
    session.query(Customer).delete()
    session.query(Employee).delete()
    session.query(Contract).delete()
    session.query(Event).delete()
    session.query(Department).delete()
    session.commit()
