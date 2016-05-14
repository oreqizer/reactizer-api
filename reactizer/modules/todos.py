from sqlalchemy import Column, Integer, String
from flask import Blueprint, request, jsonify

from reactizer.database import Base


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    text = Column(String(256))

    def __init__(self, text=None):
        self.text = text

    def __repr__(self):
        return '<Todo: %r>' % self.text


todos = Blueprint('todos', __name__)


@todos.route('/api/todos', methods=['GET', 'POST'])
def show_entries():
    if request.method == 'POST':
        """creates a new todo"""
        return jsonify(status='ok')
    else:
        """sends all todos in the database"""
        return jsonify(todos='a lot of them')