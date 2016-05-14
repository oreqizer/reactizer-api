from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/reactizer.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """import all models here that might define models so that
    they will be registered properly on the metadata.  Otherwise
    you will have to import them first before calling init_db()"""
    import reactizer.models  # NOQA
    Base.metadata.create_all(bind=engine)


def clear_db():
    """import all models here that might define models so that
    they will be registered properly on the metadata.  Otherwise
    you will have to import them first before calling init_db()"""
    import reactizer.models  # NOQA
    Base.metadata.drop_all(bind=engine)
