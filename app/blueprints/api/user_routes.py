from .import bp as api
from app.models import User
from flask import make_response, request, g, abort
from .auth_routes import basic_auth

#post put delete for user

@api.post('/register')
def register():
    user_dict = request.get_json()
    if not all(key in user_dict for key in ('first_name','last_name','email','password')):
        abort(400)
    user = User()
    user.from_dict(user_dict)
    user.save()
    return make_response(f"User {user.first_name.title()} {user.last_name.title()} was created with an id {user.id}", 200)

#login route will use this get token function
@api.get('/token')
@basic_auth.login_required()
def get_token():
    token = g.current_user.get_token()
    return make_response({"token":token}, 200)


@api.get('/login')
@basic_auth.login_required()
def get_login():
    user = g.current_user
    token = user.get_token()
    return make_response({"token":token, **user.to_dict()}, 200)


@api.put('/user/<int:id>')
@basic_auth.login_required()
def edit_user(id):
    edit_data = request.get_json()
    user = User.query.get(id)
    if not user:
        abort(404)
    if not user.id == g.current_user.id:
        abort(403)
    user.edit(edit_data['user_dict'])
    user.save()
    return make_response(f"User ID: {user.id} has been changed", 200)


@api.delete('/user/<int:id>')
@basic_auth.login_required()
def delete_user(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    if not user.user.id == g.current_user.id:
        abort(403)
    user.delete()
    return make_response(f"User with ID: {id} was deleted", 200)