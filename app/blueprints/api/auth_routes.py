from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from flask import g
from .import bp as api

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

# @api.get()
@basic_auth.verify_password
def verify_password(email, password):
    u = User.query.filter_by(email=email).first()
    if u is None:
        return False
    g.current_user = u
    return u.check_password_hash(password)

@token_auth.verify_token
def verify_token(token):
    u = User.check_token(token) if token else None
    g.current_user = u
    return u