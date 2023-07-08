from flask import Flask, jsonify, request, current_app
from flask_cors import CORS, cross_origin
from wms import *
import json

app = Flask(__name__)
CORS(app)
wms = Application()


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

@app.route('/')
def home():
    """ Home Page of the app """
    return jsonify({"message": "Hello world!"}), 200

@app.route('/menu', methods=['GET'])
def get_menu():
    """ Gets the restaurant menu """
    return call(None, wms.menu_handler.jsonify)

@app.route('/menu/categories', methods=['GET'])
def get_categories():
    """ Gets the menu categories """
    return call(None, wms.menu_handler.jsonify_categories)

@app.route('/menu/categories', methods=['POST'])
def create_category():
    """ Creates a new menu category

    JSON FORMAT:
    {
        "name": "string"
    }
    """
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        obj = request.json
    else:
        return jsonify({"error": "Incorrect content-type"}), 400

    return call({"message": f"Successfully added category {obj['name']}"},
                    wms.menu_handler.add_category, obj["name"])

@app.route('/menu/categories/<category>', methods=['GET'])
def get_category(category):
    """ Gets a specific menu category """
    return call(None, wms.menu_handler.jsonify_category, category)

@app.route('/menu/categories/<category>', methods=['POST'])
def add_menu_item_to_category(category):
    """ Adds a new menu item to a specific category

    JSON FORMAT:
    {
        "name": "string",
        "price": float,
        "image_url": "string"
    }
    """
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        obj = request.json
        try:
            name = obj["name"]
            price = obj["price"]
            imageURL = obj["image_url"]
        except:
            return jsonify({"error": "Incorrect fields"}), 400
        
        return call({"message": f"Successfully added menuitem {name}"},
                        wms.menu_handler.add_menu_item, category, name, price, imageURL)

@app.route('/menu/categories/<category>', methods=['DELETE'])
def delete_category(category):
    """ Removes a specific category """
    return call({"message": f"Successfully deleted category {category}"},
                wms.menu_handler.remove_category, category)
    
@app.route('/menu/categories/<category>/<menu_item>', methods=['GET'])
def get_menu_item(category, menu_item):
    """ Gets a specific menu item from a specific category """
    return call(None, wms.menu_handler.jsonify_menu_item, category, menu_item)

@app.route('/menu/categories/<category>/<menu_item>', methods=['DELETE'])
def delete_menu_item(category, menu_item):
    """ Removes a specific menu item from a specific category """
    return call({"message": f"Successfully removed menuitem {menu_item} in category {category})"},
                wms.menu_handler.remove_menu_item, category, menu_item)

@app.route('/menu/deals', methods=['GET'])
def get_deal():
    """ Gets a menu deal """
    return call(None, wms.menu_handler.jsonify_deals)

@app.route('/menu/deals', methods=['POST'])
def create_deal():
    """ Creates a new menu deal

    JSON FORMAT:
    {
        "discount": int,
        "menu_items": [{"name": "string"},{"name": "string"},...]
    }
    
    """
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        obj = request.json
        # Check if all menu items exist
        try: 
            menu_item_lookup = [i["name"] for i in obj["menu_items"]]
        except:
            return jsonify({"error": "Incorrect fields"})
        
        return call({"message": f"Successfully added deal"},
                        wms.menu_handler.add_deal, obj["discount"], menu_item_lookup)
    
    else:
        return jsonify({"error": "Incorrect content-type"}), 400

@app.route('/table', methods=['GET'])
def get_table():
    """ Gets all of the restaurant tables """
    return call(None, wms.table_handler.jsonify)

@app.route('/table/add', methods=['POST'])
def add_table():
    """ Creates a new table

    JSON FORMAT:
    {
        "table_limit": int,
        "orders": List[Order]
    }
    """
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        obj = request.json
        try:
            table_limit = obj["table_limit"]
            orders = obj["orders"]
        except:
            return jsonify({"error": "Incorrect fields"}), 400
        
        return call({"message": "Successfully added table"},
                    wms.table_handler.add_table, table_limit, orders)
        
    else:
        return jsonify({"error": "Incorrect content-type"}), 400

@app.route('/user', methods=['GET'])
def get_user():
    """ Gets all of the restaurant users """
    return call(None, wms.user_handler.jsonify)

@app.route('/user/add', methods=['POST'])
def add_user():
    """ Creates a new user

    JSON FORMAT:
    {
        "first_name": string,
        "last_name": string,
        "user_type": string
    }
    """ 
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        obj = request.json
        try:
            first_name = obj["first_name"]
            last_name = obj["last_name"]
            user_type = obj["user_type"]
        except:
            return jsonify({"error": "Incorrect fields"}), 400
        
        return call({"message": f"Successfully added user {first_name} {last_name}"},
                    wms.user_handler.add_user, first_name, last_name, user_type)
        
    else:
        return jsonify({"error": "Incorrect content-type"}), 400
    
@app.route('/table/add/customer', methods=['POST'])
def add_table_customer():
    """ Adds a customer to a table

    JSON FORMAT:
    {
        "table_id": int,
        "customer_id": int
    }
    """ 
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        obj = request.json
        try:
            table_id = obj["table_id"]
            customer_id = obj["customer_id"]
        except:
            return jsonify({"error": "Incorrect fields"}), 400
        
        return call({"message": "Successfully added customer to table"},
                    wms.table_handler.add_customer, table_id, wms.user_handler.id_to_user(customer_id))
        
    else:
        return jsonify({"error": "Incorrect content-type"}), 400
    
#### ORDER MANAGER ENDPOINTS
    
@app.route('/ordermanager', methods=['GET'])
def get_order_manager():
    """ Gets the order manager """
    return call(None, wms.om_handler.jsonify)
    
@app.route('/ordermanager/orders', methods=['GET'])
def get_orders():
    """ Gets the list of orders present in the order manager """
    return call(None, wms.om_handler.jsonify_orders), 200

@app.route('/ordermanager/orders/add/<table_id>' , methods=['POST'])
def add_order(table_id):
    """ Adds an order to the order manager with the table it belongs to

    JSON FORMAT:
    { 
        "menu_items: [{"id": int}, ... , {"id": int}],
        "deals:      [{"id": int}, ... , {"id": int}] 
    }
    """
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        obj = request.json
        try:
            menu_items_ids = [i["id"] for i in obj["menu_items"]]
            deals_ids = [i["id"] for i in obj["deals"]]
        except:
            return jsonify({"error": "Incorrect fields"}), 400
        
        return call({"message": "Successfully added order"},
                     wms.om_handler.add_order, table_id, menu_items_ids, deals_ids)
    
    else:
        return jsonify({"error": "Incorrect content-type"}), 400
    
@app.route('/ordermanager/orders/remove/<table_id>/<order_id>', methods=['DELETE'])
def remove_order(table_id, order_id):
    """ Removes an order from the order manager """
    return call({"message": "Successfully deleted order"},
                 wms.om_handler.remove_order, table_id, order_id)
    
@app.route('/ordermanager/tables/<table_id>', methods=['GET'])
def get_table_orders(table_id):
    """ Gets all the orders of a specific table """
    return call(None, wms.om_handler.get_table_orders, table_id)


@app.route('/ordermanager/tables/<table_id>/bill', methods=['GET'])
def get_table_bill(table_id):
    """ Gets the bill for a table 

    EMPTY POST REQUEST. NO DATA EXPECTED
    """
    return call(None, wms.om_handler.calculate_and_return_bill, table_id)

@app.route('/ordermanager/tables/<table_id>/bill', methods=['POST'])
def pay_table_bill(table_id):
    """ Endpoint to simulate bill payment for a table """
    return call({"message": "Successfully paid bill"},
                    wms.om_handler.pay_table_bill, table_id)
    
@app.route("/ordermanager/orders/<order_id>", methods=['GET'])
def get_order_by_id(order_id):
    """ Gets an order by its ID value """
    return call(None, wms.om_handler.get_order_by_id, order_id)

@app.route("/ordermanager/orders/<order_id>", methods=['DELETE'])
def delete_order_by_id(order_id):
    """ Deletes an order by its ID value """
    return call({"message": "Successfully removed order from ordermanager"},
                wms.om_handler.delete_order_by_id, order_id)
    
@app.route("/ordermanager/orders/<order_id>/state", methods=['GET'])
def get_order_state(order_id):
    """ Gets the current state of an order """
    return call(None, wms.om_handler.get_order_state, order_id)

@app.route("/ordermanager/orders/<order_id>/state", methods=['POST'])
def advance_order_state(order_id):
    """ Advances the state of a particular order

    EMPTY FOR NOW. WE WILL EXPAND THIS LATER TO INCLUDE STATE LEAPS IF WE WANT
    """
    return call({"message": "Successfully changed state"},
                wms.om_handler.change_order_state, order_id)

@app.route('/ordermanager/orders/<order_id>/<menu_item_id>/state', methods=['GET'])
def get_menu_item_state(order_id, menu_item_id):
    return call(None, wms.om_handler.get_menu_item_state, order_id, menu_item_id)

@app.route('/ordermanager/orders/<order_id>/<menu_item_id>/state', methods=['POST'])
def change_menu_item_state(order_id, menu_item_id):
    return call({"message": "Successfully changed state"},
                wms.om_handler.change_menu_item_state, order_id, menu_item_id)

@app.route("/ordermanager/orders/<order_id>/bill", methods=['GET'])
def get_order_bill(order_id):
    """ Gets the bill for an order """
    return call(None, wms.om_handler.get_order_bill, order_id)

@app.route("/ordermanager/orders/<order_id>/bill", methods=['POST'])
def pay_order_bill(order_id):
    """ Endpoint to simulate bill payment for an order """
    return call({"message": "Successfully paid bill"},
                wms.om_handler.pay_order_bill, order_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)