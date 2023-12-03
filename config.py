class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking

    SECRET_KEY = 'secret_key'
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    # database URL
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'


class TestingConfig(Config):
    TESTING = True
    # fake database URL
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
