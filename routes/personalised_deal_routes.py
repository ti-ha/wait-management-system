from flask import Blueprint
from wms import *
from globals import backend, token_optional, token_required, call
from flask import request, jsonify, session

deals_blueprint = Blueprint("deals", __name__)

# Just a testing route
@deals_blueprint.route("/personalised/dataset", methods = ['GET'], endpoint='calculate_dataset')
def calculate_dataset():
    return call(
        None,
        backend.pd_engine.load_data
    )

# Just a testing route
@deals_blueprint.route("/personalised/generate/<item_id>", methods = ['GET'], endpoint='calculate_prediction_for_id')
def calculate_prediction_for_id(item_id):
    return call(
        None,
        backend.pd_engine.generate_prediction,
        session['user_id'],
        int(item_id)
    )