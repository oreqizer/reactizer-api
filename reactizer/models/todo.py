from reactizer.database import db
from reactizer.keys.db import DbKeys
from reactizer.tools.mixins import ModelMixin


class Todo(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(256), nullable=False)
    done = db.Column(db.Boolean, nullable=False)

    def __setattr__(self, key, value):
        protected = ['id', 'user_id']
        if key in protected:
            raise KeyError(str(DbKeys.protected_key))

        super().__setattr__(key, value)

    def __init__(self, **kwargs):
        self.user = kwargs['user']
        self.text = kwargs['text']
        self.done = False

    def __repr__(self):
        return '<Todo: %r>' % self.text
