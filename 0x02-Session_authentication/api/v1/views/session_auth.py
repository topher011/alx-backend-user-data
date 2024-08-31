#!/usr/bin/env python3
'''
handles all routes for the Session authentication.
'''
from api.v1.views import app_views
from flask import request, make_response, jsonify
from models.user import User
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=True)
def login():
    '''
    Login authentication Route
    '''
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if email is None or email == "":
        resp = make_response(jsonify({"error": "email missing"}))
        resp.status_code = 400
        return resp
    if password is None or password == "":
        resp = make_response(jsonify({"error": "password missing"}))
        resp.status_code = 400
        return resp
    try:
        user = User.search({"email": email})[0]
    except IndexError:
        user = None
    if user is None:
        resp = make_response(jsonify(
            {"error": "no user found for this email"}))
        resp.status_code = 404
        return resp
    if not user.is_valid_password(password):
        resp = make_response(jsonify(
            {"error": "wrong password"}
        ))
        resp.status_code = 401
        return resp
    session_id = auth.create_session(user.id)
    resp = make_response(jsonify(user.to_json()))
    resp.set_cookie('SESSION_NAME', session_id)
    return resp


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=True)
def logout():
    '''
    logout authentication Route
    '''
    is_deleted = auth.destroy_session(request)
    if not is_deleted:
        abort(404)
    return jsonify({})
