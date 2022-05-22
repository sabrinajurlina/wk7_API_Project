from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix='/api')

from .import book_routes, auth_routes, user_routes