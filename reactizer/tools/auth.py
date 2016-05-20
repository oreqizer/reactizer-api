import jwt
import bcrypt
from functools import wraps
from datetime import datetime, timedelta
from re import search
from flask import current_app, request, Response, g

from reactizer.models.users import User
from reactizer.enums.roles import Role


def get_token(user):
    """creates a token for the given user with 28 day duration"""
    print(datetime.now())
    return jwt.encode(dict(
        iss=current_app.config['JWT_ISS'],
        sub=user.id,
        iat=datetime.now() - timedelta(hours=10),
        exp=datetime.now() + timedelta(hours=10),
    ), current_app.config['SECRET_KEY']).decode('utf-8')


def decode_token(token):
    """checks if the given token is valid"""
    return jwt.decode(token, current_app.config['SECRET_KEY'])


def validate_token(token, user, role=Role.user):
    """validates the token, optionally with a role"""
    # checks token validity
    if datetime.fromtimestamp(token['exp']) < datetime.now():
        raise ValueError('auth.token_expired')

    # checks token's roles
    if user.role < role.value:
        raise ValueError('auth.no_privileges')


def hash_password(password, hashed=None):
    """creates a hash from the given password, and optionally a hash"""
    # we need to encode the password for bcrypt
    salt = hashed or bcrypt.gensalt(14)
    # and then decode to store it as string
    return bcrypt.hashpw(password, salt)


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
    if not search(r'[A-Z]', password):
        raise ValueError('auth.password.no_uppercase')

    # no lowercase letter in password
    if not search(r'[a-z]', password):
        raise ValueError('auth.password.no_lowercase')


# Decorators
# ---


def authorize(role=Role.user):
    """checks token and maybe if the bearer has permission level"""
    def decorator(f):

        @wraps(f)
        def wrapped(*args, **kwargs):
            raw_token = request.headers.get('Authorization')
            if not raw_token:
                return Response('auth.missing_token', 401)

            token = decode_token(raw_token)
            user = User.query.filter_by(id=token['sub']).first()
            try:
                validate_token(token, user, role=role)
            except ValueError as err:
                return Response(str(err), 401)

            g.user = user
            return f(*args, **kwargs)

        return wrapped
    return decorator
