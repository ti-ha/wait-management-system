from flask import Flask, jsonify, request, current_app
from flask_cors import CORS, cross_origin
from wms import *
import json

app = Flask(__name__)
CORS(app)
wms = Application()

# A lot of the logic in here needs to be refactored to a new class. Speedrunning for now to get API working for frontend

@app.route('/')
def home():
    return jsonify({"Hello world!"}), 200

@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(wms.menu_handler.jsonify()), 200

@app.route('/menu/categories', methods=['GET','POST'])
def create_category():
    if request.method == "GET":
        return jsonify(wms.menu_handler.jsonify_categories()), 200
    elif request.method == "POST":
        '''
        JSON FORMAT:
        {"name": "string"}
        '''
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            obj = request.json
            wms.menu_handler.add_category(obj["name"])
            return jsonify({"message": f"Successfully added category {obj['name']}"}), 200
        else:
            return jsonify({"error": "Incorrect content-type"}), 400

@app.route('/menu/categories/<category>', methods=['GET', 'POST', 'DELETE'])
def specific_category(category):
    if request.method == 'GET':
        return jsonify(wms.menu_handler.jsonify_category(category)), 200
    elif request.method == 'POST':
        '''
        ADDING A NEW MENU ITEM TO CATEGORY.
        JSON FORMAT:
        {"name": "string",
         "price": float  ,
         "image_url": "string"}
        '''
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            obj = request.json
            try:
                name = obj["name"]
                price = obj["price"]
                imageURL = obj["image_url"]
            except:
                return jsonify({"error": "Incorrect fields"}), 400
            
            wms.menu_handler.add_menu_item(category, name, price, imageURL)
            return jsonify({"message": f"Successfully added menuitem {name}"}), 200
        
    elif request.method == 'DELETE':
        '''
        REMOVING A SPECIFIC CATEGORY. DELETE METHOD FOR MENUITEM
        IS IN THE SPECIFIC ROUTE FOR SPECIFIC MENU ITEM
        '''
        wms.menu_handler.remove_category(category)
        return jsonify({"message": f"Successfully deleted category {category}"}), 200

    else:
        return jsonify({"error": "Not a valid request"}), 400
    
@app.route('/menu/categories/<category>/<menu_item>', methods=['GET', 'DELETE'])
def menu_item(category, menu_item):
    if wms.menu_handler.get_menu_item(category, menu_item) == None:
        return jsonify({"error": "Unrecognised menu_item"}), 400
    
    if request.method == 'GET':
        return jsonify(wms.menu_handler.jsonify_menu_item(category, menu_item)), 200
        
    elif request.method == 'DELETE':
        wms.menu_handler.remove_menu_item(category, menu_item)
        return jsonify({"message": f"Successfully removed menuitem {menu_item} in category {category})"}), 200
    else:
        return jsonify({"error": "Unrecognised request"}), 400

@app.route('/menu/deals', methods=['GET','POST'])
def create_deal():
    if request.method == 'GET':
        return jsonify(wms.menu_handler.jsonify_deals()), 200
        
    elif request.method == 'POST':
        '''
        JSON FORMAT:
        {"discount": int,
        "menu_items": [{"name": "string"},
                        {"name": "string"}
                        }]
        }
        
        '''
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            obj = request.json
            # Check if all menu items exist
            try: 
                menu_item_lookup = [i["name"] for i in obj["menu_items"]]
            except:
                return jsonify({"error": "Incorrect fields"})
            
            proc = wms.menu_handler.add_deal(obj["discount"], menu_item_lookup)
            if proc == None:
                return jsonify({"error": "One or more menu items is not present in the menu"})
            
            return jsonify({"message": f"Successfully added deal with new id {str(proc)}"}), 200
        
        else:
            return jsonify({"error": "Incorrect content-type"}), 400
    else:
        return jsonify({"error": "Unrecognised request"}), 400

@app.route('/table', methods=['GET'])
def get_table():
    return jsonify(wms.table_handler.jsonify()), 200

@app.route('/table/add', methods=['POST'])
def add_table():
    '''
    JSON FORMAT:
    {"table_limit": int,
     "orders": List<Order>}
    '''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        obj = request.json
        try:
            table_limit = obj["table_limit"]
            orders = obj["orders"]
        except:
            return jsonify({"error": "Incorrect fields"}), 400
        
        table_id = wms.table_handler.add_table(table_limit, orders)
        return jsonify({"message": f"Successfully added table {str(table_id)}"}), 200

@app.route('/user', methods=['GET'])
def get_user():
    return jsonify(wms.user_handler.jsonify()), 200

@app.route('/user/add', methods=['POST'])
def add_user():
    '''
    JSON FORMAT:
    {"first_name": string,
     "last_name": string,
     "user_type": string}
    '''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        obj = request.json
        try:
            first_name = obj["first_name"]
            last_name = obj["last_name"]
            user_type = obj["user_type"]
        except:
            return jsonify({"error": "Incorrect fields"}), 400
        
        user_id = wms.user_handler.add_user(first_name, last_name, user_type)
        if user_id == None:
            return jsonify({"error": "Unable to create user"}), 400
        return jsonify({"message": f"Successfully added user {str(user_id)}"}), 200
    
@app.route('/table/add/customer', methods=['POST'])
def add_table_customer():
    '''
    JSON FORMAT:
    {"table_id": int,
     "customer_id": int}
    '''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        obj = request.json
        try:
            table_id = obj["table_id"]
            customer_id = obj["customer_id"]
        except:
            return jsonify({"error": "Incorrect fields"}), 400
        
        status = wms.table_handler.add_customer(table_id, wms.id_to_user(customer_id))
        if not status:
            return jsonify({"error": "Unable to move customer to table"}), 400
        return jsonify({"message": "Successfully added customer to table"}), 200
    
#### ORDER MANAGER ENDPOINTS
    
@app.route('/ordermanager', methods=['GET'])
def get_order_manager():
    if request.method == 'GET':
        return jsonify(wms.om_handler.jsonify()), 200
    else:
        return jsonify({"error": "Unrecognised request"}), 400
    
@app.route('/ordermanager/orders', methods=['GET'])
def get_orders():
    if request.method == 'GET':
        return jsonify(wms.om_handler.jsonify_orders()), 200
    else:
        return jsonify({"error": "Unrecognised request"}), 400

@app.route('/ordermanager/orders/add/<table_id>' , methods=['POST'])
def add_order(table_id):
    '''
    JSON FORMAT:
    { "menu_items: [{"id": int}, ... , {"id": int}],
      "deals:      [{"id": int}, ... , {"id": int}] }
    '''
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            obj = request.json
            try:
                menu_items_ids = [i["id"] for i in obj["menu_items"]]
                deals_ids = [i["id"] for i in obj["deals"]]
            except:
                return jsonify({"error": "Incorrect fields"}), 400
            
            try:
                wms.om_handler.add_order(table_id, menu_items_ids, deals_ids)
            except ValueError:
                return jsonify({"error":"Invalid args in json"}), 400
            
            return jsonify({"message": "Successfully added order"}), 200

    else:
        return jsonify({"error": "Unrecognised request"}), 400
    
@app.route('/ordermanager/orders/remove/<table_id>/<order_id>', methods=['DELETE'])
def remove_order(table_id, order_id):
    if request.method == 'DELETE':
        try:
            wms.om_handler.remove_order(table_id, order_id)
        except:
            return jsonify({"error": "Bad request (See backend server for details)"}), 400
        
        return jsonify({"message": "Successfully deleted order"}), 200
    else:
        return jsonify({"error": "Unrecognised request"}), 400
    
@app.route('/ordermanager/tables/<table_id>', methods=['GET'])
def get_table_orders(table_id):
    if request.method == 'GET':
        try:
            output = wms.om_handler.get_table_orders(table_id)
        except Exception as e:
            return jsonify({"error": e.args}), 400
        
        return jsonify(output), 200

    else:
        return jsonify({"error":"Unrecognised request"}), 400

@app.route('/ordermanager/tables/<table_id>/bill', methods=['GET','POST'])
def manage_table_bill(table_id):
    '''
    EMPTY POST REQUEST. NO DATA EXPECTED
    '''
    if request.method == 'GET':
        try:
            output = wms.om_handler.calculate_and_return_bill(table_id)
        except Exception as e:
            return jsonify({"error": e.args}), 400

        return jsonify(output), 200

    
    elif request.method == 'POST':
        try:
            wms.om_handler.pay_table_bill(table_id)
        except Exception as e:
            return jsonify({"error": e.args}), 400
        
        return jsonify({"message": "Successfully paid bill"}), 200
    else:
        return jsonify({"error": "Unrecognised request"}), 400
    
@app.route("/ordermanager/orders/<order_id>", methods=['GET','DELETE'])
def manage_order_by_id(order_id):
    if request.method == 'GET':
        try:
            order = wms.om_handler.get_order_by_id(order_id)
        except Exception as e:
            return jsonify({"error": e.args}), 400
        return jsonify(order), 200
    
    elif request.method == 'DELETE':
        try:
            wms.om_handler.delete_order_by_id(order_id)
        except Exception as e:
            return jsonify({"error": e.args}), 400
        return jsonify({"message": "Successfully removed order from ordermanager"}), 200

    else:
        return jsonify({"error": "Unrecognised request"}), 400
    
@app.route("/ordermanager/orders/<order_id>/state", methods=['GET', 'POST'])
def affect_order_state(order_id):
    if request.method == 'GET':
        try:
            output = wms.om_handler.get_order_state(order_id)
        except Exception as e:
            return jsonify({"error": e.args}), 400
        return jsonify(output), 200
    
    elif request.method == 'POST':
        '''
        EMPTY FOR NOW. WE WILL EXPAND THIS LATER TO INCLUDE STATE LEAPS IF WE WANT
        '''
        try:
            output = wms.om_handler.change_order_state(order_id)
        except Exception as e:
            return jsonify({"error": e.args}), 400
        return jsonify({"message": f"Successfully changed state to {output}"}), 200

        
    else:
        return jsonify({"error": "Unrecognised request"}), 400

@app.route("/ordermanager/orders/<order_id>/bill", methods=['GET', 'POST'])
def manage_order_bill(order_id):
    if request.method == 'GET':
        try:
            output = wms.om_handler.get_order_bill(order_id)
        except Exception as e:
            return jsonify({"error": e.args}), 400
        
        return jsonify(output), 200
    
    elif request.method == 'POST':
        try:
            wms.om_handler.pay_order_bill(order_id)
        except Exception as e:
            return jsonify({"error": e.args}), 400
        return jsonify({"message": "Successfully paid bill"}), 200
    else:
        return jsonify({"error": "Unrecognised request"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)