from flask import Flask
from flask_cors import CORS

from reactizer.database import db
from reactizer.routes.todos import todos
from reactizer.routes.users import users


def create_app():
    app = Flask(__name__)
    CORS(app)

    # config
    app.config.from_object('reactizer.config')

    # add all blueprints from models
    app.register_blueprint(todos)
    app.register_blueprint(users)

    db.init_app(app)
    return app
