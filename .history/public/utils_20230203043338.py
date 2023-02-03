import secrets

def custom_id():
    id = secrets.token_hex(16)
    return id