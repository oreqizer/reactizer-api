from flask import Flask

from reactizer.database import db_session
from reactizer import modules


# initialize app!
app = Flask(__name__)

app.config.from_object('reactizer.config')
app.config.from_envvar('RIZER_CONFIG', silent=True)


# add all blueprints from modules
app.register_blueprint(modules.todos.todos)


# executes after the request (no shit)
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


