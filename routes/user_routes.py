from flask import Blueprint
from wms import *
from middlewares import backend, token_required, call, blacklist_token, unblacklist_token
from flask import request, jsonify, session, current_app
import jwt
import datetime

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route('/users', methods=['GET'], endpoint='get_user')
@token_required
def get_user(current_user):
    """ Gets all of the restaurant users """
    if current_user.__class__ is not Manager:
        return jsonify({"error": "Must be Manager to make this request"}), 401
    
    return call(
        None, 
        backend.user_handler.jsonify
    )

@user_blueprint.route('/me', methods=['GET'], endpoint='get_current_user')
@token_required
def get_current_user(current_user):
    """ Gets the current user of the system """
    return call(
        None,
        current_user.jsonify
    )

@user_blueprint.route('/user/add', methods=['POST'], endpoint='add_user')
def add_user():
    """ Creates a new user

    JSON FORMAT:
    {
        "first_name": string,
        "last_name": string,
        "user_type": string
        if staffmember:
            "password": string 
    }
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        try:
            first_name = obj["first_name"]
            last_name = obj["last_name"]
            user_type = obj["user_type"]
            password = obj["password"]
        except KeyError:
            return jsonify({"error": "Incorrect fields"}), 400

        return call(
            {"message": f"Successfully added user {first_name} {last_name}"},
            backend.user_handler.add_user,
            first_name,
            last_name,
            user_type,
            password
        )
    return jsonify({"error": "Incorrect content-type"}), 400

@user_blueprint.route('/user/login', methods=['POST'], endpoint='login')
def login():
    """ Logs in a user given firstname, lastname and password. Returns an auth
    token and sets the session user to the userID
    
    JSON FORMAT:
    {
        "first_name": string
        "last_name": string
        "password": string
    }
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        try:
            first_name = obj["first_name"]
            last_name = obj["last_name"]
            password = obj["password"]
        except KeyError:
            return jsonify({"error": "Incorrect fields"}), 400
        
        user = backend.user_handler.login(first_name, last_name, password)
        if user:
            # Define the session user_id
            session['user_id'] = user.id

            # Generate token
            token = jwt.encode({"user_id": user.id,
                                "expiry": str(datetime.datetime.utcnow().date())},
                        current_app.config['SECRET_KEY'],
                        algorithm="HS256")
            
            unblacklist_token(token)

            return jsonify({"message": "Success",
                            "auth_token": token}), 200
        
        return jsonify({"error": "Incorrect credentials"}), 400
    
@user_blueprint.route('/user/logout', methods=['POST'], endpoint='logout')
@token_required
def logout(current_user):
    """ Logs out the current user """
    blacklist_token(request.headers['Authorization'])
    return call(
        {"message": "Successfully logged out"},
        backend.user_handler.logout,
        current_user
    )