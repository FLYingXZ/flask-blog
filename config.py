import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "axsakdasjdausdcasw"
    SSL_DISABEL = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
                              'mysql+pymysql://root:123456@localhost:3306/db1?charset=utf8'

class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
                              'mysql+pymysql://root:123456@localhost:3306/db1?charset=utf8'

class TestingConfig(Config):
    TESTING = True
    SERVER_NAME = "localhost:5000"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
                              "sqlite:///" + os.path.join(basedir, "data-test.sqlite")
    WTF_CSRF_ENABLED = False
config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'default':DevelopmentConfig,
    'production':Production
}
