from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify

from reactizer.database import Base, db_session
from reactizer.tools.mixins import ModelMixin
from reactizer.tools import auth
from reactizer.enums import Role


class User(Base, ModelMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(72))
    email = Column(String(120), unique=True)

    def __init__(self, username=None, password=None, email=None, role=None):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def __repr__(self):
        return '<User id={}, username={}>'.format(self.id, self.username)

    def for_client(self):
        to_filter = ['password', 'id']
        return {key: self[key] for key in dict(self) if key not in to_filter}


users = Blueprint('users', __name__)


@users.route('/api/users')
@auth.check_token()
def show_users():
    """list all users"""
    results = [dict(user) for user in User.query.all()]
    return jsonify(users=results)


@users.route('/api/users/login', methods=['POST'])
def login():
    """logs a user in"""
    payload = request.get_json()
    user = User.query.filter(User.username == payload['username']).first()
    if not user:
        return 'auth.user_not_found', 401

    if user['password'] != auth.hash_password(payload['password'], hashed=user['password']):
        return 'auth.invalid_password', 401

    token = auth.get_token(user)
    return jsonify(user=user.for_client(), token=token)


@users.route('/api/users/register', methods=['POST'])
def register():
    """registers a new user"""
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
        return jsonify(user=user.for_client(), token=token)
    except IntegrityError:
        return 'auth.integrity_taken', 409

