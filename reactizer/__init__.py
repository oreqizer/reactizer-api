import os
from flask import Flask, jsonify, g, request

from reactizer.database import db_session


# initialize app!
app = Flask(__name__)

app.config.from_object('reactizer.config')
app.config.from_envvar('RIZER_CONFIG', silent=True)

print(app.config)


# executes after the request (no shit)
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/api/todos', methods=['GET', 'POST'])
def show_entries():
    if request.method == 'POST':
        """creates a new todo"""
        cur = g.db.execute('insert into todos values {}'.format(request.form['text']))
        return jsonify(status='ok')
    else:
        """sends all todos in the database"""
        cur = g.db.execute('select id, text from todos')
        entries = [dict(id=row[0], text=row[1]) for row in cur.fetchall()]
        return jsonify(todos=entries)

