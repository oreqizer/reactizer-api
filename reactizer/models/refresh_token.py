from reactizer.database import db
from reactizer.tools.mixins import ModelMixin


class RefreshToken(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    app = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(72), nullable=False)

    def __init__(self, **kwargs):
        self.user = kwargs['user']
        self.app = kwargs['app']
        self.token = kwargs['token']

    def __repr__(self):
        return '<Token: %r>' % self.text
