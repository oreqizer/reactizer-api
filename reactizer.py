import os
import sqlite3
from contextlib import closing
from flask import Flask, g


# initialize app!
app = Flask(__name__)


# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'reactizer.db'),
    DEBUG=True,
    SECRET_KEY='devops',
    USERNAME='admin',
    PASSWORD='reacTizer1337',
))
# specifies path to config folder, e.g. 'RIZER_CONFIG=config.py'
app.config.from_envvar('RIZER_CONFIG', silent=True)


# database methods
def connect_db():
    """Connects to the specific database."""
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """Initializes the database."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# executes before request
@app.before_request
def before_request():
    g.db = connect_db()


# executes after the request (no shit)
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
