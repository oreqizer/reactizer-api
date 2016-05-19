from flask import Flask

from reactizer.database import db_session
from reactizer.models.todos import todos
from reactizer.models.users import users


# initialize app
app = Flask(__name__)

app.config.from_object('reactizer.config')
app.config.from_envvar('RIZER_CONFIG', silent=True)


# add all blueprints from models
app.register_blueprint(todos)
app.register_blueprint(users)


# executes after the request (no shit)
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
