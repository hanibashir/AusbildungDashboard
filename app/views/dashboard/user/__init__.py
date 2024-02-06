from flask import Blueprint


user_blueprint = Blueprint('profile', __name__)

from app.views.auth import register, login, logout
from . import profile