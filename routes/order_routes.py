from flask import Blueprint
from wms import *
from globals import backend, token_optional, token_required, call
from flask import request, jsonify

order_blueprint = Blueprint("order", __name__)

@order_blueprint.route('/ordermanager', methods=['GET'], endpoint='get_order_manager')
@token_required
def get_order_manager(current_user):
    """ Gets the order manager """
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401
    
    return call(
        None, 
        backend.om_handler.jsonify
    )

@order_blueprint.route('/ordermanager/orders', methods=['GET'], endpoint='get_orders')
@token_required
def get_orders(current_user):
    """ Gets the list of orders present in the order manager """
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401
    
    return call(
        None, 
        backend.om_handler.jsonify_orders
    )

@order_blueprint.route('/ordermanager/orders/add/<table_id>' , methods=['POST'], endpoint='add_order')
def add_order(table_id):
    """ Adds an order to the order manager with the table it belongs to

    JSON FORMAT:
    {
        "menu_items: [{"id": int}, ... , {"id": int}],
        "deals:      [{"id": int}, ... , {"id": int}]
    }
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        try:
            menu_items_ids = [i["id"] for i in obj["menu_items"]]
            deals_ids = [i["id"] for i in obj["deals"]]
        except KeyError:
            return jsonify({"error": "Incorrect fields"}), 400
        return call(
            {"message": "Successfully added order"},
            backend.om_handler.add_order,
            int(table_id),
            menu_items_ids,
            deals_ids
        )
    return jsonify({"error": "Incorrect content-type"}), 400

@order_blueprint.route('/ordermanager/orders/remove/<table_id>/<order_id>', methods=['DELETE'], endpoint='remove_order')
@token_required
def remove_order(current_user, table_id, order_id):
    """ Removes an order from the order manager """
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401
    
    return call(
        {"message": "Successfully deleted order"},
        backend.om_handler.remove_order,
        int(table_id),
        int(order_id)
    )

@order_blueprint.route('/ordermanager/tables/<table_id>', methods=['GET'], endpoint='get_table_orders')
def get_table_orders(table_id):
    """ Gets all the orders of a specific table """
    return call(
        None, 
        backend.om_handler.get_table_orders, 
        int(table_id)
    )

@order_blueprint.route('/ordermanager/tables/<table_id>/bill', methods=['GET'], endpoint='get_table_bill')
def get_table_bill(table_id):
    """ Gets the bill for a table """
    return call(
        None, 
        backend.om_handler.calculate_and_return_bill, 
        int(table_id)
    )

@order_blueprint.route('/ordermanager/tables/<table_id>/bill', methods=['POST'], endpoint='pay_table_bill')
def pay_table_bill(table_id):
    """ Endpoint to simulate bill payment for a table 
        EMPTY POST REQUEST. NO DATA EXPECTED
    """
    return call(
        {"message": "Successfully paid bill"},
        backend.om_handler.pay_table_bill,
        int(table_id)
    )

@order_blueprint.route("/ordermanager/orders/<order_id>", methods=['GET'], endpoint='get_order_by_id')
def get_order_by_id(order_id):
    """ Gets an order by its ID value """
    return call(
        None, 
        backend.om_handler.get_order_by_id, 
        int(order_id)
    )

@order_blueprint.route("/ordermanager/orders/<order_id>", methods=['DELETE'], endpoint='delete_order_by_id')
@token_required
def delete_order_by_id(current_user, order_id):
    """ Deletes an order by its ID value """

    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401

    return call(
        {"message": "Successfully removed order from ordermanager"},
        backend.om_handler.delete_order_by_id,
        int(order_id)
    )

@order_blueprint.route("/ordermanager/orders/<order_id>/state", methods=['GET'], endpoint='get_order_state')
@token_required
def get_order_state(current_user, order_id):
    """ Gets the current state of an order """
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401
    
    return call(
        None, 
        backend.om_handler.get_order_state,
        int(order_id)
    )

@order_blueprint.route("/ordermanager/orders/<order_id>/state", methods=['POST'], endpoint='advance_order_state')
@token_required
def advance_order_state(current_user, order_id):
    """ Advances the state of a particular order

    EMPTY FOR NOW. WE WILL EXPAND THIS LATER TO INCLUDE STATE LEAPS IF WE WANT
    """
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401

    return call(
        {"message": "Successfully changed state"},
        backend.om_handler.change_order_state,
        int(order_id)
    )

@order_blueprint.route('/ordermanager/orders/<order_id>/<menu_item_id>/state', methods=['GET'], endpoint='get_menu_item_state')
@token_required
def get_menu_item_state(current_user, order_id, menu_item_id):
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401
    
    return call(
        None, 
        backend.om_handler.get_menu_item_state, 
        int(order_id), 
        int(menu_item_id)
    )

@order_blueprint.route('/ordermanager/orders/<order_id>/<menu_item_id>/state', methods=['POST'], endpoint='change_menu_item_state')
@token_required
def change_menu_item_state(current_user, order_id, menu_item_id):

    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401
    
    return call(
        {"message": "Successfully changed state"},
        backend.om_handler.change_menu_item_state, 
        int(order_id), 
        int(menu_item_id)
    )

@order_blueprint.route("/ordermanager/orders/<order_id>/bill", methods=['GET'], endpoint='get_order_bill')
def get_order_bill(order_id):
    """ Gets the bill for an order """
    return call(
        None, 
        backend.om_handler.get_order_bill, 
        int(order_id)
    )

@order_blueprint.route("/ordermanager/orders/<order_id>/bill", methods=['POST'], endpoint='pay_order_bill')
def pay_order_bill(order_id):
    """ Endpoint to simulate bill payment for an order """
    return call(
        {"message": "Successfully paid bill"},
        backend.om_handler.pay_order_bill,
        int(order_id)
    )