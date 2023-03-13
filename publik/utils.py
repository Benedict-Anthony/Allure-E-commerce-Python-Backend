import secrets

def custom_id():
    id = secrets.token_hex(10)
    return id