import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    CELERY_BROKER_URL="redis://127.0.0.1:6379/1"
    CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/2"
    REDIS_URL="redis://127.0.0.1:6379"

class LocalDevelopmentConfig(Config):
    # SQLITE_DB_DIR = os.path.join(basedir)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'database.sqlite3')
    DEBUG = True
    SECRET_KEY =  'Random Hashed Key' #Strong,random and should be in the evn
    SECURITY_PASSWORD_HASH = "bcrypt"    
    SECURITY_PASSWORD_SALT = 'Other Random Hashed Key' # Read from ENV in your case
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_DEFAULT_REMEMBER_ME=False
    SECURITY_UNAUTHORIZED_VIEW = None
    # SECURITY_POST_LOGOUT_VIEW = '/login'
    # SECURITY_POST_LOGIN_VIEW = '/dashboard'
    # SECURITY_POST_REGISTER_VIEW = '/login'
    WTF_CSRF_ENABLED = False
    REDIS_URL="redis://127.0.0.1:6379"


class StageConfig(Config):
    # SQLITE_DB_DIR = os.path.join(basedir)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'database.sqlite3')
    DEBUG = True
    SECRET_KEY =  'Random Hashed Key' #Strong,random and should be in the evn
    SECURITY_PASSWORD_HASH = "bcrypt"    
    SECURITY_PASSWORD_SALT = 'Other Random Hashed KEY' # Read from ENV in your case
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_DEFAULT_REMEMBER_ME=False
    SECURITY_UNAUTHORIZED_VIEW = None
    # SECURITY_POST_LOGOUT_VIEW = '/login'
    # SECURITY_POST_LOGIN_VIEW = '/dashboard'
    # SECURITY_POST_REGISTER_VIEW = '/login'
    WTF_CSRF_ENABLED = False
    REDIS_URL="redis://127.0.0.1:6379"
