from flask import Flask
from flask_session import Session
from config import Config
from instance.database import db
from flask_migrate import Migrate
from app.views import blog, dashboard
from app.views.dashboard import dashboard_blueprint
from app.views.blog import blog_blueprint
from app.views.dashboard.user import user_blueprint


# function to create the app (application factory function)
def create_app():
    # create and configure the app
    app = Flask(__name__)

    app.config.from_object(Config)

    # Initialize database connection with the app
    db.init_app(app)
    # migration
    migrate = Migrate(app=app, db=db)

    Session(app)

    # register the views
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(user_blueprint)

    # import api_queries models
    from .models.user import User
    from .models.post import Post
    from .models.page import Page
    from .models.category import Category
    from .models.role import Role
    from .models.user_role import UserRole
    # create api_queries tables
    with app.app_context():
        db.create_all()

    return app
