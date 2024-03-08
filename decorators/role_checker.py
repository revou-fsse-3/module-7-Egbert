from flask_login import current_user
from functools import wraps

def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated and current_user.role == role_name:
                return func(*args, **kwargs)
            else:
                return "Unauthorized", 403
        return wrapper
    return decorator