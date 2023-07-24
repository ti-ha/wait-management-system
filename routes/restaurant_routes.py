from flask import Blueprint
from wms import *
from globals import backend, token_optional, token_required, call
from flask import request, jsonify

restaurant_blueprint = Blueprint("restaurant", __name__)

@restaurant_blueprint.route('/restaurant/table/size', methods=['GET'], endpoint='sort_table_size')
@token_required
def sort_table_size(current_user):
    """ Sorts restaurant tables by table size """
    if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401
    
    return call(
        None,
        backend.restaurant_manager_handler.tables_sort_size
    )

@restaurant_blueprint.route('/restaurant/table/orders', methods=['GET'], endpoint='sort_table_orders')
@token_required
def sort_table_orders(current_user):
    """ Sorts restaurant tables by lowest order status of the table """
    if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401
    
    return call(
        None,
        backend.restaurant_manager_handler.tables_sort_orders
    )

@restaurant_blueprint.route('/restaurant/staff/position', methods=['GET'], endpoint='sort_staff_position')
@token_required
def sort_staff_position(current_user):
    """ Sorts restaurant staff members by position """
    if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401
    
    return call(
        None,
        backend.restaurant_manager_handler.staff_sort_position
    )

@restaurant_blueprint.route('/restaurant/staff/status', methods=['GET'], endpoint='sort_staff_status')
@token_required
def sort_staff_status(current_user):
    """ Sorts restaurant staff members by status """
    if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401
    
    return call(
        None,
        backend.restaurant_manager_handler.staff_sort_status
    )

@restaurant_blueprint.route('/restaurant/menu/stats', methods=['GET'], endpoint='get_menu_stats')
@token_required
def get_menu_stats(current_user):
    """ Prints out menu item order frequency statistics """
    if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401
    
    return call(
        None,
        backend.restaurant_manager_handler.get_menu_stats
    )