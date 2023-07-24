from flask import Blueprint
from wms import *
from globals import backend, token_optional, token_required, call
from flask import request, jsonify

deals_blueprint = Blueprint("deals", __name__)

@deals_blueprint.route("/personalised/dataset", methods = ['GET'], endpoint='calculate_dataset')
def calculate_dataset():
    return call(
        None,
        backend.pd_engine.load_data
    )