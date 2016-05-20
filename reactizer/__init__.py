from flask import Flask

from reactizer.database import db
from reactizer.routes.todos import todos
from reactizer.routes.users import users


def create_app():
    app = Flask(__name__)

    # config
    app.config.from_object('reactizer.config')
    app.config.from_envvar('RIZER_CONFIG', silent=True)

    # add all blueprints from models
    app.register_blueprint(todos)
    app.register_blueprint(users)

    db.init_app(app)
    return app
