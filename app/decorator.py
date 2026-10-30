from functools import wraps
from flask import request, abort
from app.models import User
from flask_login import current_user


def permission_required(permissions_list):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not any(current_user.can(p) for p in permissions_list):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
