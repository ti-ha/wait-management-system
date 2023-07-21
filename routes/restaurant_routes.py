from flask import Blueprint
from wms import *
from globals import backend, token_optional, token_required, call
from flask import request, jsonify

restaurant_blueprint = Blueprint("restaurant", __name__)

### Your routes here