from flask import Blueprint

aus_page_blueprint = Blueprint('aus_page', __name__)

from . import post_routes
