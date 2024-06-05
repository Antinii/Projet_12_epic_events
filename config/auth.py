from config.settings import SECRET_KEY, DATABASE_URL
from models.employees import Employee
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import config.session_manager as session_manager
import jwt
import datetime


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

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
        return payload['sub'], False
    except jwt.ExpiredSignatureError:
        return None, True
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None

def get_logged_in_user(token):
    employee_id, is_expired = decode_token(token)
    if employee_id:
        return session.query(Employee).filter_by(id=employee_id).first(), is_expired
    return None, is_expired

def logout():
    session_manager.clear_current_token()
    from views.main_view import main
    main()
