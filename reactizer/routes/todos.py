from flask import Blueprint, request, jsonify, g
from flask_babel import gettext

from reactizer.database import db
from reactizer.models.todo import Todo
from reactizer.tools import auth

todos = Blueprint('todos', __name__)


@todos.route('/api/todos', methods=['GET', 'POST'])
@auth.authorize()
def list_or_add():
    """created a new Todo, or lists all user's ones"""
    if request.method == 'POST':
        todo = Todo(**request.get_json(), user=g.user)
        db.session.add(todo)
        db.session.commit()
        return jsonify(todo)
    else:
        todo_list = Todo.query.filter_by(user_id=g.user.id)
        results = [dict(todo) for todo in todo_list]
        return jsonify(todos=results)


@todos.route('/api/todos/<int:todo_id>', methods=['PUT', 'DELETE'])
@auth.authorize()
def manipulate(todo_id):
    """updates or deletes a todo"""
    todo = Todo.query.get(todo_id)
    if not todo:
        return gettext('No such todo.'), 404

    if todo.user_id != g.user.id:
        return gettext('This todo doesn\'t belong to you.'), 401

    if request.method == 'PUT':
        changes = request.get_json()
        for key in changes:
            todo[key] = changes[key]

        db.session.commit()
        return jsonify(todo)
    else:
        db.session.delete(todo)
        db.session.commit()
        return jsonify(status='ok')
