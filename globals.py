from wms import *
from flask import Flask, jsonify, request, current_app
import jwt
from functools import wraps

backend = Application()

def token_required(f):
    """Performs authentication for methods that REQUIRE authentication.

    Args:
        f (func): View function to be executed

    Returns:
        func: The decorated function
    """
    @wraps(f)
    def inner(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        
        if not token:
            
            return jsonify({
                "message": "Authentication Token missing",
                "error": "Unauthorized"
            }), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = backend.user_handler.id_to_user(data["user_id"])
            if current_user is None:
                return jsonify({
                    "message": "Invalid Authentication token",
                    "error": "Unauthorized"
                }), 401
        except Exception as e:
            return jsonify({
                "message": "Something went wrong",
                "error": str(e)
            }), 500
        
        return f(current_user, *args, **kwargs)
    
    return inner


def token_optional(f):
    """Performs authentication for methods that do not require 
    but can benefit from authentication.

    Args:
        f (func): View function to be executed

    Returns:
        func: The decorated function
    """
    @wraps(f)
    def inner(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        
        if not token:
            return f(None, *args, **kwargs)
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = backend.user_handler.id_to_user(data["user_id"])
            if current_user is None:
                return jsonify({
                    "message": "Invalid Authentication token",
                    "error": "Unauthorized"
                }), 401
        
        except Exception as e:
            return jsonify({
                "message": "Something went wrong",
                "error": str(e)
            }), 500
        
        return f(current_user, *args, **kwargs)
    
    return inner

def call(msg, func, *args):
    """ Attempts to run a function func, returning a msg if it succeeds with no output.

    Args:
        msg (dict): Success message if no output
        func (function): function to be called
        *args (tuple): list of args to call to func

    Returns:
        json: the response to be sent to the frontend,
        int: the response code
    """
    try:
        output = func(*args)
    except Exception as e:
        # Uncomment this line for debugging
        raise e
        return jsonify({"error": e.args}), 400

    if output is not None:
        return jsonify(output), 200

    else:
        return jsonify(msg), 200
