from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from reactizer.config import DB_URI
from reactizer.models import User
from reactizer.tools import auth
from reactizer.enums import Role


engine = create_engine(DB_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """import all models here that might define models so that
    they will be registered properly on the metadata.  Otherwise
    you will have to import them first before calling init_db()"""
    from reactizer import models  # NOQA
    Base.metadata.create_all(bind=engine)


def clear_db():
    Base.metadata.drop_all(bind=engine)


def init_masteruser():
    pwd = auth.hash_password('Default1337')
    user = User(username='oreqizer',
                email='test@test.com',
                password=pwd,
                role=Role.master.value)

    db_session.add(user)
    db_session.commit()
