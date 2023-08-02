from flask import Blueprint
from wms import *
from middlewares import backend, token_required, call
from flask import request, jsonify

table_blueprint = Blueprint("table", __name__)

@table_blueprint.route('/table', methods=['GET'], endpoint='get_table')
def get_table():
    """ Gets all of the restaurant tables """

    return call(
        None, 
        backend.table_handler.jsonify
    )

@table_blueprint.route('/table/add', methods=['POST'], endpoint='add_table')
@token_required
def add_table(current_user):
    """ Creates a new table

    JSON FORMAT:
    {
        "table_limit": int,
        "orders": List[Order]
    }
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        try:
            table_limit = obj["table_limit"]
            orders = obj["orders"]
        except KeyError:
            return jsonify({"error": "Incorrect fields"}), 400
        
        if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401

        return call(
            {"message": "Successfully added table"},
            backend.table_handler.add_table,
            table_limit,
            orders
        )
    return jsonify({"error": "Incorrect content-type"}), 400

@table_blueprint.route('/table/add/customer', methods=['POST'], endpoint='add_table_customer')
def add_table_customer():
    """ Adds a customer to a table

    JSON FORMAT:
    {
        "table_id": int,
        "customer_id": int
    }
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        try:
            table_id = obj["table_id"]
            customer_id = obj["customer_id"]
        except KeyError:
            return jsonify({"error": "Incorrect fields"}), 400
        return call(
            {"message": "Successfully added customer to table"},
            backend.table_handler.add_customer,
            table_id,
            backend.user_handler.id_to_user(customer_id)
        )
    return jsonify({"error": "Incorrect content-type"}), 400