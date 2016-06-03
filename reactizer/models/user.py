from reactizer.database import db
from reactizer.tools.mixins import ModelMixin
from reactizer.enums.roles import Role


class User(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(72))
    email = db.Column(db.String(120), unique=True, nullable=False)
    todos = db.relationship('Todo', backref='user')
    refresh_tokens = db.relationship('RefreshToken', backref='refresh_token')
    role = db.Column(db.Integer)

    def __init__(self, role=Role.user.value, **kwargs):
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.email = kwargs['email']
        self.role = role

    def __repr__(self):
        return '<User id={}, username={}>'.format(self.id, self.username)

    def for_user(self):
        to_filter = ['password', 'id', 'role']
        return {key: self[key] for key in dict(self) if key not in to_filter}

    def for_admin(self):
        to_filter = ['password']
        return {key: self[key] for key in dict(self) if key not in to_filter}
