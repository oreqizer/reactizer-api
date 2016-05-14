import bcrypt
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify

from reactizer.database import Base, db_session
from reactizer.tools.mixins import DictMixin
from reactizer.tools.auth import check_password, decode_user


class User(Base, DictMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(72))
    email = Column(String(120), unique=True)

    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


users = Blueprint('users', __name__)


@users.route('/api/users/register', methods=['POST'])
def register():
    """registers a new user"""
    payload = request.get_json()
    password = payload['password']
    # checks password validity
    try:
        check_password(password)
    except ValueError as err:
        return jsonify(status='error', msg=str(err))

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
    payload['password'] = hashed
    # guards if username/email are available
    try:
        user = User(**payload)
        db_session.add(user)
        db_session.commit()
    except IntegrityError:
        return jsonify(status='error', msg='auth.integrity_taken')

    return jsonify(status='ok')


@users.route('/api/users')
def show_users():
    """list all users"""
    results = [decode_user(user.as_dict()) for user in User.query.all()]
    return jsonify(users=results)
