import os
# pwd
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    Holds config information for the app. The general pattern followed is to first check the value of an
    environment variable and if not set use a default value
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # the location of the file where the db data will be stored
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # If True, sends a signal to the app everytime a change is about to be made in the db
    SQLALCHEMY_TRACK_MODIFICATIONS = False