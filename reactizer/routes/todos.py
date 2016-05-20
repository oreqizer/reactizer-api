from flask import Blueprint, request, jsonify

from reactizer.database import db
from reactizer.models.todos import Todo

todos = Blueprint('todos', __name__)


@todos.route('/api/todos', methods=['GET', 'POST'])
def list_add_todos():
    if request.method == 'POST':
        """creates a new todo"""
        todo = Todo(**request.get_json())
        db.add(todo)
        db.commit()
        return jsonify(status='ok')
    else:
        """sends all todos in the database"""
        results = [dict(todo) for todo in Todo.query.all()]
        return jsonify(todos=results)
