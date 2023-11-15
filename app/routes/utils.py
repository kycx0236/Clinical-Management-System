from functools import wraps
from flask_login import current_user
from flask import abort

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != required_role:
                abort(403) 
            return func(*args, **kwargs)
        return wrapper
    return decorator
