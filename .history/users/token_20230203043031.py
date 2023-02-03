from datetime import datetime, timedelta
from django.conf import settings
import jwt
import secrets

def user_token(payload):
    token = jwt.encode(
        {"exp":datetime.utcnow() + timedelta(days=2), "payload":payload},
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return token


def decode_token(token):
    try:
        token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return token
    except Exception as exec:
        return None
    
def custom_id():
    id = secrets.token_hex(16)
    return id