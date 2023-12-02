from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# init SQLAlchemy
db = SQLAlchemy()


# function to create the app (application factory function)
def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database connection with the app
    db.init_app(app)

    # TODO: Import and register app blueprints
    # Import blueprints
    from .api.users import user_blueprint
    from .api.aus_pages import aus_page_blueprint
    from .api.categories import category_blueprint
    # Register blueprints
    app.register_blueprint(user_blueprint)
    app.register_blueprint(aus_page_blueprint)
    app.register_blueprint(category_blueprint)

    # create db tables
    from .models.user import User
    from .models.aus_page import AusPage
    from .models.page import Page
    from .models.category import Category
    from .models.role import Role
    from .models.user_role import UserRole
    with app.app_context():
        db.create_all()

    return app
