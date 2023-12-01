
class Config:
    # database URL
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking

    SECRET_KEY = 'secret_key'
    DEBUG = False

