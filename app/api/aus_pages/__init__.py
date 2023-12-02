from flask import Blueprint

aus_page_blueprint = Blueprint('aus_page', __name__)

from . import aus_page_routes
