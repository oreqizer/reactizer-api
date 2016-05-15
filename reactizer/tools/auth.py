import jwt
import bcrypt
from functools import wraps
from datetime import datetime, timedelta
from re import search
from flask import current_app, request, Response, jsonify

from reactizer.consts import roles


def get_token(user):
    """creates a token for the given user with 28 day duration"""
    return jwt.encode(dict(
        iss=user['id'],
        exp=datetime.now() + timedelta(days=28)
    ), current_app.config['SECRET_KEY']).decode('utf-8')


def decode_token(token):
    """checks if the given token is valid"""
    return jwt.decode(token, current_app.config['SECRET_KEY'])


def validate_token(token, role=None):
    """validates the token, optionally with a role"""
    # checks token presence
    if not token:
        raise ValueError('auth.missing_token')

    decoded = decode_token(token)
    # checks token validity
    if decoded['exp'] < datetime.now():
        raise ValueError('auth.token_expired')

    # checks token's audience
    if role and roles[decoded['aud']] < roles[role]:
        raise ValueError('auth.no_privileges')


def hash_password(password, hashed=None):
    salt = hashed or bcrypt.gensalt(14)
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def check_password(password):
    """checks password's strength"""
    # password too long
    if len(password) > 32:
        raise ValueError('auth.password.too_long')

    # password too short
    if len(password) < 8:
        raise ValueError('auth.password.too_short')

    # no number in password
    if not search(r'\d', password):
        raise ValueError('auth.password.no_number')

    # no uppercase letter in password
    print(password)
    if not search(r'[A-Z]', password):
        raise ValueError('auth.password.no_uppercase')

    # no lowercase letter in password
    if not search(r'[a-z]', password):
        raise ValueError('auth.password.no_lowercase')


# Decorators
# ---


def check_token(f):
    """checks the presence and validity of JWT token"""
    wraps(f)

    def wrapped(*args, **kwargs):
        payload = request.get_json()
        try:
            validate_token(payload['token'])
        except ValueError as err:
            Response(str(err), 401)

        return f(*args, **kwargs)

    return wrapped


def check_token_role(role):
    """checks if the bearer has permission level"""
    def decorator(f):
        wraps(f)

        def wrapped(*args, **kwargs):
            payload = request.get_json()
            try:
                validate_token(payload['token'], role=role)
            except ValueError as err:
                Response(str(err), 401)

            return f(*args, **kwargs)

        return wrapped

    return decorator
