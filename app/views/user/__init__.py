from flask import Blueprint


user_blueprint = Blueprint('user', __name__)

from ..auth import register, login, logout
from . import profile