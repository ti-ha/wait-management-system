from flask import Blueprint
from wms import *
from middlewares import backend, call
from flask import session

deals_blueprint = Blueprint("deals", __name__)

@deals_blueprint.route("/personalised/deals", methods = ['GET'], endpoint='calculate_prediction_for_id')
def calculate_prediction_for_id():
    """ Creates personalised deals for the current user """
    return call(
        None,
        backend.pd_engine.make_deals,
        session['user_id']
    )