import os

DEBUG = os.environ.get('DEBUG') or True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'potato'

# DB stuff
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or\
                          'postgres://oreqizer@localhost/reactizer'

# JWT sutff
JWT_ISS = os.environ.get('JWT_ISS') or 'reactizer'

# Babel
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC'
