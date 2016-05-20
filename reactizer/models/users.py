from reactizer.database import db
from reactizer.tools.mixins import ModelMixin


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(72))
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.Integer)

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
