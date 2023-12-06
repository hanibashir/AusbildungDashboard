from flask import Blueprint

page_blueprint = Blueprint('page', __name__)

from . import page_routes
