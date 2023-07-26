from flask import Blueprint
from wms import *
from globals import backend, call
from flask import session

deals_blueprint = Blueprint("deals", __name__)

# Just a testing route
@deals_blueprint.route("/personalised/deals", methods = ['GET'], endpoint='calculate_prediction_for_id')
def calculate_prediction_for_id():
    return call(
        None,
        backend.pd_engine.make_deals,
        session['user_id']
    )