from models.employees import Employee
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import jwt
import datetime

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
session = Session()

SECRET_KEY = "your_secret_key"

def generate_token(employee_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'sub': employee_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_logged_in_user(token):
    employee_id = decode_token(token)
    if employee_id:
        return session.query(Employee).filter_by(id=employee_id).first()
    return None
