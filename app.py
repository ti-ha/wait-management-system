from functools import wraps
from flask import Flask, jsonify, request, current_app
from flask_cors import CORS, cross_origin
from wms import *
import json, jwt, datetime

app = Flask(__name__)
CORS(app)
wms = Application()

SECRET_KEY = "RomanticCheese"
app.config['SECRET_KEY'] = SECRET_KEY


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

def token_required(f):
    """Performs authentication for methods that REQUIRE authentication.

    Args:
        f (func): View function to be executed

    Returns:
        func: The decorated function
    """
    @wraps(f)
    def inner(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        
        if not token:
            
            return jsonify({
                "message": "Authentication Token missing",
                "error": "Unauthorized"
            }), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = wms.user_handler.id_to_user(data["user_id"])
            if current_user is None:
                return jsonify({
                    "message": "Invalid Authentication token",
                    "error": "Unauthorized"
                }), 401
        except Exception as e:
            return jsonify({
                "message": "Something went wrong",
                "error": str(e)
            }), 500
        
        return f(current_user, *args, **kwargs)
    
    return inner


def token_optional(f):
    """Performs authentication for methods that do not require 
    but can benefit from authentication.

    Args:
        f (func): View function to be executed

    Returns:
        func: The decorated function
    """
    @wraps(f)
    def inner(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        
        if not token:
            return f(None, *args, **kwargs)
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = wms.user_handler.id_to_user(data["user_id"])
            if current_user is None:
                return jsonify({
                    "message": "Invalid Authentication token",
                    "error": "Unauthorized"
                }), 401
        
        except Exception as e:
            return jsonify({
                "message": "Something went wrong",
                "error": str(e)
            }), 500
        
        return f(current_user, *args, **kwargs)
    
    return inner

@app.route('/')
def home():
    """ Home Page of the app """
    return jsonify({"message": "Hello world!"}), 200

@app.route('/menu', methods=['GET'], endpoint='get_menu')
def get_menu():
    """ Gets the restaurant menu """

    return call(
        None, 
        wms.menu_handler.jsonify
    )

@app.route('/menu/categories', methods=['GET'], endpoint='get_categories')
def get_categories():
    """ Gets the menu categories """
    return call(
        None, 
        wms.menu_handler.jsonify_categories
    )

@app.route('/menu/categories', methods=['POST'], endpoint='create_category')
@token_required
def create_category(current_user):
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
    
    if current_user.__class__ is not Manager:
        return jsonify({"error": "Must be Manager to make this request"})

    return call(
        {"message": f"Successfully added category {obj['name']}"},
        wms.menu_handler.add_category,
        obj["name"]
    )

@app.route('/menu/categories/<category>', methods=['GET'])
def get_category(category):
    """ Gets a specific menu category """
    return call(
        None, 
        wms.menu_handler.jsonify_category, 
        category
    )

@app.route('/menu/categories/<category>', methods=['PATCH'], endpoint='update_category')
@token_required
def update_category(current_user, category):
    """ Updates a menu category with a new name or visibility status
    Note that to set the category visible use the exact string "True", anything
    else will set the visible boolean to False

    JSON FORMAT:
    {
        "new_name": "string",
        "visible": "string"
    }
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        
        new_name = obj["new_name"] if "new_name" in obj else None
        visible = obj["visible"] if "visible" in obj else None

        if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401

        return call(
            {"message": f"Successfully updated category"},
            wms.menu_handler.update_category,
            category,
            new_name,
            visible
        )

@app.route('/menu/categories/order', methods=['POST'], endpoint='reorder_categories')
@token_required
def reorder_categories(current_user):
    """ Rearranges the categorie in the menu

    JSON FORMAT:
    {
        "new_order": List[String]
    }
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        try:
            new_order = obj["new_order"]
        except KeyError:
            return jsonify({"error": "Incorrect fields"}), 400
        
        if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401

        return call(
            {"message": f"Successfully reordered categories"},
            wms.menu_handler.reorder_category,
            new_order
        )
    return None

@app.route('/menu/categories/<category>', methods=['POST'], endpoint='add_menu_item_to_category')
@token_required
def add_menu_item_to_category(current_user, category):
    """ Adds a new menu item to a specific category

    JSON FORMAT:
    {
        "name": "string",
        "price": float,
        "image_url": "string"
    }
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        try:
            name = obj["name"]
            price = obj["price"]
            image_url = obj["image_url"]
        except KeyError:
            return jsonify({"error": "Incorrect fields"}), 400
        
        if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401

        return call(
            {"message": f"Successfully added menuitem {name}"},
            wms.menu_handler.add_menu_item,
            category,
            name,
            price,
            image_url
        )
    return None

@app.route('/menu/categories/<category>', methods=['DELETE'], endpoint='delete_category')
@token_required
def delete_category(current_user, category):
    """ Removes a specific category """

    if current_user.__class__ is not Manager:
        return jsonify({"error": "Must be Manager to make this request"}), 401

    return call(
        {"message": f"Successfully deleted category {category}"},
        wms.menu_handler.remove_category,
        category
    )

@app.route('/menu/categories/<category>/order', methods=['POST'], endpoint='reorder_menu_items')
@token_required
def reorder_menu_items(current_user, category):
    """ Rearranges the categorie in the menu

    JSON FORMAT:
    {
        "new_order": List[String]
    }
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        try:
            new_order = obj["new_order"]
        except KeyError:
            return jsonify({"error": "Incorrect fields"}), 400
        
        if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401

        return call(
            {"message": f"Successfully reordered menu items"},
            wms.menu_handler.reorder_menu_items,
            category,
            new_order
        )
    return None

@app.route('/menu/categories/<category>/<menu_item>', methods=['GET'], endpoint='get_menu_item')
def get_menu_item(category, menu_item):
    """ Gets a specific menu item from a specific category """
    return call(None, wms.menu_handler.jsonify_menu_item, category, menu_item)

@app.route('/menu/categories/<category>/<menu_item>', methods=['DELETE'], endpoint='delete_menu_item')
@token_required
def delete_menu_item(current_user, category, menu_item):
    """ Removes a specific menu item from a specific category """
    if current_user.__class__ is not Manager:
        return jsonify({"error": "Must be Manager to make this request"}), 401

    return call(
        {"message": f"Successfully removed menuitem {menu_item} in category {category}"},
        wms.menu_handler.remove_menu_item,
        category,
        menu_item
    )

@app.route('/menu/categories/<category>/<menu_item>', methods=['PATCH'], endpoint='update_menu_item')
@token_required
def update_menu_item(current_user, category, menu_item):
    """ Updates a menu category with a new name or visibility status
    Note that to set the category visible use the exact string "True", anything
    else will set the visible boolean to False

    JSON FORMAT:
    {
        "new_name": "string",
        "price": "string",
        "image_url": "string",
        "visible": "string"
    }
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        
        new_name = obj["new_name"] if "new_name" in obj else None
        price = obj["price"] if "price" in obj else None
        image_url = obj["image_url"] if "image_url" in obj else None
        visible = obj["visible"] if "visible" in obj else None

        if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401

        return call(
            {"message": f"Successfully updated menu item"},
            wms.menu_handler.update_menu_item,
            category,
            menu_item,
            new_name,
            price,
            image_url,
            visible
        )

@app.route('/menu/deals', methods=['GET'], endpoint='get_deal')
def get_deal():
    """ Gets a menu deal """
    return call(
        None, 
        wms.menu_handler.jsonify_deals
    )

@app.route('/menu/deals', methods=['POST'], endpoint='create_deal')
@token_required
def create_deal(current_user):
    """ Creates a new menu deal

    JSON FORMAT:
    {
        "discount": float,
        "menu_items": [{"name": "string"},{"name": "string"},...]
    }

    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        # Check if all menu items exist
        try:
            menu_item_lookup = [i["name"] for i in obj["menu_items"]]
        except KeyError:
            return jsonify({"error": "Incorrect fields"})
        
        if current_user.__class__ is not Manager:
            return jsonify({"error": "Must be Manager to make this request"}), 401

        return call(
            {"message": "Successfully added deal"},
            wms.menu_handler.add_deal,
            obj["discount"],
            menu_item_lookup
        )
    return jsonify({"error": "Incorrect content-type"}), 400

@app.route('/menu/search', methods=['GET'], endpoint='search_menu')
def search_menu():
    query = request.args.get('query')

    return call(
        None, 
        wms.menu_handler.search,
        query
    )
    

@app.route('/table', methods=['GET'], endpoint='get_table')
def get_table():
    """ Gets all of the restaurant tables """

    return call(
        None, 
        wms.table_handler.jsonify
    )

@app.route('/table/add', methods=['POST'], endpoint='add_table')
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
            wms.table_handler.add_table,
            table_limit,
            orders
        )
    return jsonify({"error": "Incorrect content-type"}), 400

@app.route('/users', methods=['GET'], endpoint='get_user')
@token_required
def get_user(current_user):
    """ Gets all of the restaurant users """
    if current_user.__class__ is not Manager:
        return jsonify({"error": "Must be Manager to make this request"}), 401
    
    return call(
        None, 
        wms.user_handler.jsonify
    )

@app.route('/me', methods=['GET'], endpoint='get_current_user')
@token_required
def get_current_user(current_user):
    return call(
        None,
        current_user.jsonify
    )

@app.route('/user/add', methods=['POST'], endpoint='add_user')
def add_user():
    """ Creates a new user

    JSON FORMAT:
    {
        "first_name": string,
        "last_name": string,
        "user_type": string
        if staffmember:
            "password": string 
    }
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        try:
            first_name = obj["first_name"]
            last_name = obj["last_name"]
            user_type = obj["user_type"]
            password = obj["password"]
        except KeyError:
            return jsonify({"error": "Incorrect fields"}), 400

        return call(
            {"message": f"Successfully added user {first_name} {last_name}"},
            wms.user_handler.add_user,
            first_name,
            last_name,
            user_type,
            password
        )
    return jsonify({"error": "Incorrect content-type"}), 400

@app.route('/user/login', methods=['POST'], endpoint='login')
def login():
    """logs in a user given firstname, lastname and password. returns an auth token
    
    JSON FORMAT:
    {
        "first_name": string
        "last_name": string
        "password": string
    }
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        try:
            first_name = obj["first_name"]
            last_name = obj["last_name"]
            password = obj["password"]
        except KeyError:
            return jsonify({"error": "Incorrect fields"}), 400
        
        user = wms.user_handler.login(first_name, last_name, password)
        if user:
            return jsonify({"message": "Success",
                            "auth_token": jwt.encode(
                                            {"user_id": user.id,
                                             "expiry": str(datetime.datetime.utcnow().date())},
                                            app.config['SECRET_KEY'],
                                            algorithm="HS256"
                            )}), 200
        return jsonify({"error": "Incorrect credentials"}), 400
    
@app.route('/table/add/customer', methods=['POST'], endpoint='add_table_customer')
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
            wms.table_handler.add_customer,
            table_id,
            wms.user_handler.id_to_user(customer_id)
        )
    return jsonify({"error": "Incorrect content-type"}), 400

#### ORDER MANAGER ENDPOINTS

@app.route('/ordermanager', methods=['GET'], endpoint='get_order_manager')
@token_required
def get_order_manager(current_user):
    """ Gets the order manager """
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401
    
    return call(
        None, 
        wms.om_handler.jsonify
    )

@app.route('/ordermanager/orders', methods=['GET'], endpoint='get_orders')
@token_required
def get_orders(current_user):
    """ Gets the list of orders present in the order manager """
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401
    
    return call(
        None, 
        wms.om_handler.jsonify_orders
    )

@app.route('/ordermanager/orders/add/<table_id>' , methods=['POST'], endpoint='add_order')
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
            wms.om_handler.add_order,
            int(table_id),
            menu_items_ids,
            deals_ids
        )
    return jsonify({"error": "Incorrect content-type"}), 400

@app.route('/ordermanager/orders/remove/<table_id>/<order_id>', methods=['DELETE'], endpoint='remove_order')
@token_required
def remove_order(current_user, table_id, order_id):
    """ Removes an order from the order manager """
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401
    
    return call(
        {"message": "Successfully deleted order"},
        wms.om_handler.remove_order,
        int(table_id),
        int(order_id)
    )

@app.route('/ordermanager/tables/<table_id>', methods=['GET'], endpoint='get_table_orders')
def get_table_orders(table_id):
    """ Gets all the orders of a specific table """
    return call(
        None, 
        wms.om_handler.get_table_orders, 
        int(table_id)
    )

@app.route('/ordermanager/tables/<table_id>/bill', methods=['GET'], endpoint='get_table_bill')
def get_table_bill(table_id):
    """ Gets the bill for a table """
    return call(
        None, 
        wms.om_handler.calculate_and_return_bill, 
        int(table_id)
    )

@app.route('/ordermanager/tables/<table_id>/bill', methods=['POST'], endpoint='pay_table_bill')
def pay_table_bill(table_id):
    """ Endpoint to simulate bill payment for a table 
        EMPTY POST REQUEST. NO DATA EXPECTED
    """
    return call(
        {"message": "Successfully paid bill"},
        wms.om_handler.pay_table_bill,
        int(table_id)
    )

@app.route("/ordermanager/orders/<order_id>", methods=['GET'], endpoint='get_order_by_id')
def get_order_by_id(order_id):
    """ Gets an order by its ID value """
    return call(
        None, 
        wms.om_handler.get_order_by_id, 
        int(order_id)
    )

@app.route("/ordermanager/orders/<order_id>", methods=['DELETE'], endpoint='delete_order_by_id')
@token_required
def delete_order_by_id(current_user, order_id):
    """ Deletes an order by its ID value """

    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401

    return call(
        {"message": "Successfully removed order from ordermanager"},
        wms.om_handler.delete_order_by_id,
        int(order_id)
    )

@app.route("/ordermanager/orders/<order_id>/state", methods=['GET'], endpoint='get_order_state')
@token_required
def get_order_state(current_user, order_id):
    """ Gets the current state of an order """
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401
    
    return call(
        None, 
        wms.om_handler.get_order_state,
        int(order_id)
    )

@app.route("/ordermanager/orders/<order_id>/state", methods=['POST'], endpoint='advance_order_state')
@token_required
def advance_order_state(current_user, order_id):
    """ Advances the state of a particular order

    EMPTY FOR NOW. WE WILL EXPAND THIS LATER TO INCLUDE STATE LEAPS IF WE WANT
    """
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401

    return call(
        {"message": "Successfully changed state"},
        wms.om_handler.change_order_state,
        int(order_id)
    )

@app.route('/ordermanager/orders/<order_id>/<menu_item_id>/state', methods=['GET'], endpoint='get_menu_item_state')
@token_required
def get_menu_item_state(current_user, order_id, menu_item_id):
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401
    
    return call(
        None, 
        wms.om_handler.get_menu_item_state, 
        int(order_id), 
        int(menu_item_id)
    )

@app.route('/ordermanager/orders/<order_id>/<menu_item_id>/state', methods=['POST'], endpoint='change_menu_item_state')
@token_required
def change_menu_item_state(current_user, order_id, menu_item_id):

    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a staff member to make this request"}), 401
    
    return call(
        {"message": "Successfully changed state"},
        wms.om_handler.change_menu_item_state, 
        int(order_id), 
        int(menu_item_id)
    )

@app.route("/ordermanager/orders/<order_id>/bill", methods=['GET'], endpoint='get_order_bill')
def get_order_bill(order_id):
    """ Gets the bill for an order """
    return call(
        None, 
        wms.om_handler.get_order_bill, 
        int(order_id)
    )

@app.route("/ordermanager/orders/<order_id>/bill", methods=['POST'], endpoint='pay_order_bill')
def pay_order_bill(order_id):
    """ Endpoint to simulate bill payment for an order """
    return call(
        {"message": "Successfully paid bill"},
        wms.om_handler.pay_order_bill,
        int(order_id)
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)