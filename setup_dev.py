from reactizer import create_app, db
from reactizer import models
from reactizer.tools import auth
from reactizer.enums.roles import Role


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run...
        # http://stackoverflow.com/questions/19437883
        db.drop_all()
        db.create_all()
        pwd = auth.hash_password('Default1337')
        user = models.user.User(username='oreqizer',
                                email='test@test.com',
                                password=pwd,
                                app='demo',
                                role=Role.master.value)

        db.session.add(user)
        db.session.commit()
