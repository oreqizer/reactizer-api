import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
from re import search
from flask import current_app, request, Response, g
from flask_babel import gettext

from reactizer.enums.roles import Role
from reactizer.models.user import User


def get_token(user):
    """creates a token for the given user with 28 day duration"""
    return jwt.encode(dict(
        iss=current_app.config['JWT_ISS'],
        sub=user.id,
        iat=datetime.utcnow(),
        exp=datetime.utcnow() + timedelta(hours=10),
    ), current_app.config['SECRET_KEY']).decode('utf-8')


def decode_token(token):
    """checks if the given token is valid"""
    return jwt.decode(token, current_app.config['SECRET_KEY'])


def validate_user(user, role=Role.user):
    """validates the token, optionally with a role"""
    # checks token's roles
    if user.role < role.value:
        raise ValueError(gettext('No privileges.'))


def hash_password(password, hashed=None):
    """creates a hash from the given password, and optionally a hash"""
    salt = hashed or bcrypt.gensalt(14)
    return bcrypt.hashpw(password, salt)


def check_password(password):
    """checks password's strength"""
    # password too long
    if len(password) > 32:
        raise ValueError(gettext('Password too long.'))

    # password too short
    if len(password) < 8:
        raise ValueError(gettext('Password too short.'))

    # no number in password
    if not search(r'\d', password):
        raise ValueError(gettext(
            'Password has to contain a number.'
        ))

    # no uppercase letter in password
    if not search(r'[A-Z]', password):
        raise ValueError(gettext(
            'Password has to contain an uppercase letter.'
        ))

    # no lowercase letter in password
    if not search(r'[a-z]', password):
        raise ValueError(gettext(
            'Password has to contain a lowercase letter.'
        ))


# Decorators
# ---


def authorize(role=Role.user):
    """checks token and maybe if the bearer has permission level"""
    def decorator(f):

        @wraps(f)
        def wrapped(*args, **kwargs):
            raw_token = request.headers.get('Authorization')
            if not raw_token:
                return Response(gettext(
                    'No token in "Authorization" header.'
                ), 401)

            token = decode_token(raw_token)
            user = User.query.get(token['sub'])
            try:
                validate_user(user, role=role)
            except ValueError as err:
                return Response(str(err), 401)

            g.user = user
            return f(*args, **kwargs)

        return wrapped
    return decorator
