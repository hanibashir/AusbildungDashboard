class Config:
    SESSION_PERMANENT = False
    # Configure session to use filesystem (instead of signed cookies)
    SESSION_TYPE = "filesystem"
    # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
    # The maximum number of items the session stores
    # before it starts deleting some, default 500
    SESSION_FILE_THRESHOLD = 100
    IMAGES_UPLOAD_FOLDER = "static/images"
    POSTS_UPLOAD_FOLDER = "static/images/posts"
    USERS_UPLOAD_FOLDER = "static/images/users"
    CATS_UPLOAD_FOLDER = "static/images/category"

    # DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ausbildung.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking

