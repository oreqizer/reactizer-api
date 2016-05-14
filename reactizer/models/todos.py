from sqlalchemy import Column, Integer, String
from reactizer.database import Base


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    text = Column(String(256))

    def __init__(self, text=None):
        self.text = text

    def __repr__(self):
        return '<Todo: %r>' % self.text