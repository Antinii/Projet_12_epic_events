current_token = None

def get_current_token():
    global current_token
    return current_token

def set_current_token(token):
    global current_token
    current_token = token
