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
    DEFAULT_POST_IMAGE = "static/images/default_post_image.png"

    USERS_UPLOAD_FOLDER = "static/images/users"
    DEFAULT_USER_IMAGE = "static/images/user-blue-thumbnail.png"

    CATEGORY_UPLOAD_FOLDER = "static/images/category"
    DEFAULT_CATEGORY_IMAGE = "static/images/default_category_image.png"

    # DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ausbildung.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking

