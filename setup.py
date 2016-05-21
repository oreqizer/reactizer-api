from reactizer import create_app, db


def setup():
    app = create_app()
    with app.app_context():
        db.create_all()


def teardown():
    app = create_app()
    with app.app_context():
        db.drop_all()

