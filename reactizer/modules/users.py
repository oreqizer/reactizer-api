import bcrypt
from sqlalchemy import Column, Integer, String
from flask import Blueprint, request, jsonify

from reactizer.database import Base, db_session
from reactizer.tools.mixins import DictMixin
from reactizer.tools.auth import check_password


class User(Base, DictMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(50), unique=True)
    password = Column(String(50))
    email = Column(String(120), unique=True)

    def __init__(self, nickname=None, password=None, email=None):
        self.nickname = nickname
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.nickname


users = Blueprint('users', __name__)


@users.route('/api/auth/register', methods=['POST'])
def show_entries():
    """registers a new user"""
    payload = request.get_json()
    password = payload['password']
    # checks password validity
    try:
        check_password(password)
    except ValueError as err:
        print(err)
        return jsonify(status='error', msg='ok')

    hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))
    user = User(**payload, password=hashed)
    db_session.add(user)
    db_session.commit()
    return jsonify(status='ok')
