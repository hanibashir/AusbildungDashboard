from flask import Blueprint

category_blueprint = Blueprint('category', __name__)

from . import category_routes
