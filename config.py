import os
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Set Flask configuration vars."""

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://fyyur:fyyur@localhost:5432/fyyurdb'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'any string works here'

    SESSION_COOKIE_SECURE = True

    SESSION_COOKIE_NAME = 'YourAppName-WebSession'

    WTF_CSRF_TIME_LIMIT = None
