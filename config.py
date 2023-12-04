class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking
    SECRET_KEY = 'secret_key'
    # ENV = 'testing'
    ENV = 'development'


class DevelopmentConfig(Config):
    DEBUG = True
    # database URL
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'


class TestingConfig(Config):
    DEBUG = True
    # Temporary database URL
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig:
    pass
