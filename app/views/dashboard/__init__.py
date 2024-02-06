from flask import Blueprint

dashboard_blueprint = Blueprint('dashboard', __name__)

from . import home
from .post import create_post
