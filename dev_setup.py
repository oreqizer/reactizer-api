from reactizer.database import Base, engine, db_session
from reactizer import models
from reactizer.tools import auth
from reactizer.enums.roles import Role


def init_db():
    Base.metadata.create_all(bind=engine)


def clear_db():
    Base.metadata.drop_all(bind=engine)


def init_masteruser():
    pwd = auth.hash_password('Default1337')
    user = models.users.User(username='oreqizer',
                             email='test@test.com',
                             password=pwd,
                             role=Role.master.value)

    db_session.add(user)
    db_session.commit()

if __name__ == "__main__":
    clear_db()
    init_db()
    init_masteruser()
