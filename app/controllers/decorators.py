from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user, login_required

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.role not in allowed_roles and current_user.role != 'admin':
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('root.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
