import secrets
from functools import wraps
from flask import session, request, abort


def generate_csrf_token():
    """Generate or retrieve CSRF token from session."""
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']


def validate_csrf(f):
    """Decorator that validates CSRF token on POST/PUT/DELETE requests."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ('POST', 'PUT', 'DELETE'):
            token = request.form.get('_csrf_token') or request.headers.get('X-CSRFToken')
            if not token or token != session.get('_csrf_token'):
                abort(403)
        return f(*args, **kwargs)
    return decorated_function
