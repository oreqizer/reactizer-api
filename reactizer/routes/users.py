from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from reactizer.database import db
from reactizer.keys.auth import AuthKeys
from reactizer.models.user import User
from reactizer.models.refresh_token import RefreshToken
from reactizer.tools import auth

users = Blueprint('users', __name__)


@users.route('/api/users/login', methods=['POST'])
def login():
    """logs a user in.
    :returns the user info and user's token
    """
    payload = request.get_json()
    user = User.query.filter(User.username == payload['username']).first()
    if not user:
        return str(AuthKeys.no_such_user), 401

    pw_hash = auth.hash_password(payload['password'], hashed=user['password'])
    if user['password'] != pw_hash:
        return str(AuthKeys.invalid_password), 401

    token = auth.get_token(user)
    # TODO: also send refresh_token
    return jsonify(user=user.for_user(), token=token)


@users.route('/api/users/register', methods=['POST'])
def register():
    """registers a new user.
    :returns the user info and user's token
    """
    payload = request.get_json()
    password = payload['password']
    # checks password validity
    try:
        auth.check_password(password)
    except ValueError as err:
        return str(err), 409

    payload['password'] = auth.hash_password(password)
    # guards if username/email are available
    try:
        user = User(**payload)
        # TODO: generate and store/send refresh token
        db.session.add(user)
        db.session.commit()
        token = auth.get_token(user)
        return jsonify(user=user.for_user(), token=token)
    except IntegrityError:
        return str(AuthKeys.integrity_taken), 409
