import jwt
from datetime import datetime, timedelta
from re import search
from flask import current_app


def get_token(user):
    """creates a token for the given user with 28 day duration"""
    return jwt.encode(dict(
        iss=user['id'],
        exp=datetime.now() + timedelta(days=28)
    ), current_app.config['SECRET_KEY']).decode('utf-8')


def check_token(token=None, idnum=None):
    """checks if the given token belongs to the bearer"""
    decoded = jwt.decode(token, current_app.config['SECRET_KEY'])

    # checks if the token matches the supplied id
    if decoded['iss'] != idnum:
        raise ValueError('auth.token.unauthorized')

    # checks if the token is not expired
    if decoded['exp'] > datetime.now():
        raise ValueError('auth.token.expired')


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
