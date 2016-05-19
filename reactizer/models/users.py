from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify, g

from reactizer.database import Base, db_session
from reactizer.tools.mixins import ModelMixin
from reactizer.tools import auth
from reactizer.enums.roles import Role


class User(Base, ModelMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(72))
    email = Column(String(120), unique=True)
    role = Column(Integer)

    def __init__(self, username=None, password=None, email=None, role=None):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def __repr__(self):
        return '<User id={}, username={}>'.format(self.id, self.username)

    def for_user(self):
        to_filter = ['password', 'id', 'role']
        return {key: self[key] for key in dict(self) if key not in to_filter}

    def for_admin(self):
        to_filter = ['password']
        return {key: self[key] for key in dict(self) if key not in to_filter}


users = Blueprint('users', __name__)


@users.route('/api/users/<user_id>')
@auth.authorize(Role.user)
def show_user(user_id):
    """:returns the requested user"""
    user = User.query.filter_by(id=user_id).first()
    if g.token['iss'] != user.id:
        return 'auth.not_owner', 401

    return jsonify(user.for_user()) if user else 'api.users.not_found', 404


@users.route('/api/users/login', methods=['POST'])
def login():
    """logs a user in.
    :returns the user info and user's token
    """
    payload = request.get_json()
    user = User.query.filter(User.username == payload['username']).first()
    if not user:
        return 'auth.user_not_found', 401

    pw_hash = auth.hash_password(payload['password'], hashed=user['password'])
    if user['password'] != pw_hash:
        return 'auth.invalid_password', 401

    token = auth.get_token(user)
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
        return jsonify(status='error', msg=str(err))

    payload['password'] = auth.hash_password(password)
    # guards if username/email are available
    try:
        user = User(**payload)
        db_session.add(user)
        db_session.commit()
        token = auth.get_token(user)
        return jsonify(user=user.for_user(), token=token)
    except IntegrityError:
        return 'auth.integrity_taken', 409


# Admin routes
# ---


@users.route('/api/admin/users/<user_id>')
@auth.authorize(Role.admin)
def show_user_admin(user_id):
    """:returns the requested user for admin"""
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user.for_admin()) if user else 'api.users.not_found', 404


@users.route('/api/admin/users')
@auth.authorize(Role.admin)
def show_users_admin():
    """:returns all users"""
    results = [user.for_admin() for user in User.query.all()]
    return jsonify(users=results)
