from flask import Blueprint

dashboard_blueprint = Blueprint('dashboard', __name__)

from . import home
from .post import create_post, edit_post
from .category import create_category, edit_category
