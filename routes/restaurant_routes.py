from flask import Blueprint
from wms import *
from globals import backend, token_optional, token_required, call
from flask import request, jsonify

restaurant_blueprint = Blueprint("restaurant", __name__)

### Your routes here
@restaurant_blueprint.route('/restaurant/table/size', methods=['GET'], endpoint='sort_table_size')
@token_required
def sort_table_size(current_user):
    if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401
    
    return call(
        None,
        backend.restaurant_manager_handler.tables_sort_size
    )

@restaurant_blueprint.route('/restaurant/table/orders', methods=['GET'], endpoint='sort_table_orders')
@token_required
def sort_table_orders(current_user):
    if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401
    
    return call(
        None,
        backend.restaurant_manager_handler.tables_sort_orders
    )