from reactizer.database import db
from reactizer.tools.mixins import ModelMixin


class Todo(ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(256))
    done = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        self.user = kwargs['user']
        self.text = kwargs['text']
        self.done = False

    def __repr__(self):
        return '<Todo: %r>' % self.text

