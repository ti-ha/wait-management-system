from flask import Flask, jsonify, request, current_app
from wms import *
import json

app = Flask(__name__)

wms = Application()
ordermanager = OrderManager()

# A lot of the logic in here needs to be refactored to a new class. Speedrunning for now to get API working for frontend

@app.route('/')
def home():
    return "Hello world!"

@app.route('/menu', methods=['GET'])
def get_menu():
    return current_app.response_class(wms.menu_json(), mimetype="application/json")

@app.route('/menu/categories', methods=['GET','POST'])
def create_category():
    if request.method == "GET":
        return current_app.response_class(wms.jsonify_menu_categories(), mimetype="application/json")
    elif request.method == "POST":
        '''
        JSON FORMAT:
        {"name": "string"}
        '''
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            obj = request.json
            wms.add_menu_category(obj["name"])
            return ("Successfully added category " + obj["name"])
        else:
            return "Incorrect content-type"

@app.route('/menu/categories/<category>', methods=['GET', 'POST', 'DELETE'])
def specific_category(category):
    if request.method == 'GET':
        return current_app.response_class(wms.jsonify_menu_category(category), mimetype="application/json")
    elif request.method == 'POST':
        '''
        ADDING A NEW MENU ITEM TO CATEGORY.
        JSON FORMAT:
        {"name": "string",
         "price": float}
        '''
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            obj = request.json
            try:
                name = obj["name"]
                price = obj["price"]
            except:
                return "Incorrect fields"
            
            wms.add_menu_item(category, name, price)
            return ("Successfully added menuitem " + name)
        
    elif request.method == 'DELETE':
        '''
        REMOVING A SPECIFIC CATEGORY. DELETE METHOD FOR MENUITEM
        IS IN THE SPECIFIC ROUTE FOR SPECIFIC MENU ITEM
        '''
        wms.remove_menu_category(category)
        return ("Successfully deleted category" + category)

    else:
        return "Not a valid request"
    
@app.route('/menu/categories/<category>/<menu_item>', methods=['GET', 'DELETE'])
def menu_item(category, menu_item):
    if wms.menu_item(category, menu_item) == None:
        return "Unrecognised menu_item"
    
    if request.method == 'GET':
        return current_app.response_class(wms.menu_item_json(category, menu_item), mimetype="application/json")
        
    elif request.method == 'DELETE':
        wms.remove_menu_item(category, menu_item)
        return "Successfully removed menuitem "+menu_item+" in category "+category
    else:
        return "Unrecognised request"

@app.route('/menu/deals', methods=['GET','POST'])
def create_deal():
    if request.method == 'GET':
        return current_app.response_class(wms.get_deals_json(), mimetype="application/json")
        
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
                return "Incorrect fields"
            
            proc = wms.add_deal(obj["discount"], menu_item_lookup)
            if proc == None:
                return "One or more menu items is not present in the menu"
            
            return ("Successfully added deal with new id "+str(proc))
        
        else:
            return "Incorrect content-type"
    else:
        return "Unrecognised request"

@app.route('/table', methods=['GET'])
def get_table():
    return current_app.response_class(wms.get_tables_json(), mimetype="application/json")

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
            return "Incorrect fields"
        
        table_id = wms.add_table(table_limit, orders)
        return ("Successfully added table " + str(table_id))

@app.route('/user', methods=['GET'])
def get_user():
    return current_app.response_class(wms.get_users_json(), mimetype="application/json")

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
            return "Incorrect fields"
        
        user_id = wms.add_user(first_name, last_name, user_type)
        if user_id == None:
            return "Unable to create user"
        return ("Successfully added user " + str(user_id))
    
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
            return "Incorrect fields"
        
        status = wms.add_table_customer(table_id, customer_id)
        if not status:
            return "Unable to move customer to table"
        return ("Successfully added customer to table")
    
#### ORDER MANAGER ENDPOINTS
    
@app.route('/ordermanager', methods=['GET'])
def get_order_manager():
    if request.method == 'GET':
        return jsonify(ordermanager.jsonify()), 200
    else:
        return jsonify("Unrecognised request"), 403
    
@app.route('/ordermanager/orders', methods=['GET'])
def get_orders():
    if request.method == 'GET':
        return jsonify(ordermanager.orders_json()), 200
    else:
        return jsonify("Unrecognised request"), 403

@app.route('/ordermanager/orders/add/<table_id>', methods=['POST'])
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
                return jsonify("Incorrect fields"), 403
            
            table = wms.id_to_table(int(table_id))
            if table == None:
                return jsonify("Table does not exist"), 403
            
            menu_items = []
            for i in menu_items_ids:
                item = wms.get_menu_item_by_id(i)
                if item == None:
                    return jsonify("MenuItem doees not exist"), 403
                else:
                    menu_items.append(item)

            deals = []
            for i in deals_ids:
                deal = wms.get_deal_by_id(i)
                if deal == None:
                    return jsonify("Deal does not exist"), 403
                else:
                    deals.append(deal)

            order = Order(menu_items, deals)

            ordermanager.add_order(order, table)
            return jsonify("Successfully added order"), 200

    else:
        return jsonify("Unrecognised request"), 403
    
@app.route('/ordermanager/orders/remove/<table_id>/<order_id>', methods=['DELETE'])
def remove_order(table_id, order_id):
    tID = int(table_id)
    oID = int(order_id)
    if request.method == 'DELETE':
        table = wms.id_to_table(tID)
        order = ordermanager.get_order(oID)
        if (table == None or order == None):
            return jsonify("Incorrect fields"), 403
        try:
            ordermanager.remove_order(order, table)
        except:
            return jsonify("Order either doesn't exist or is not assigned to a table"), 403
        
        return jsonify("Successfully deleted order"), 200
    else:
        return jsonify("Unrecognised request"), 403
    
@app.route('/ordermanager/tables/<table_id>', methods=['GET'])
def get_table_orders(table_id):
    tID = int(table_id)
    if request.method == 'GET':
        try:
            orders = ordermanager.get_table_orders(tID)
        except ValueError:
            return jsonify("table_id does not exist in map"), 403
        
        output = {"orders": []}
        for i in orders:
            output["orders"].append(i.jsonify())
        return jsonify(output), 200

    else:
        return jsonify("Unrecognised request"), 403

@app.route('/ordermanager/tables/<table_id>/bill', methods=['GET','POST'])
def manage_table_bill(table_id):
    '''
    EMPTY POST REQUEST. NO DATA EXPECTED
    '''
    tID = int(table_id)
    if request.method == 'GET':
        try:
            bill = ordermanager.calculate_table_bill(tID)
        except TypeError:
            return jsonify("Not a valid table_id"), 403
        except ValueError:
            return jsonify("One or more orders have not been served yet. Try paying for each bill individually"), 403
        
        wms.id_to_table(tID).set_bill(bill)
        output = {"price": bill.get_price(), "is_paid": bill.is_paid()}
        return jsonify(output), 200

    
    elif request.method == 'POST':
        table = wms.id_to_table(tID)
        if table == None:
            return jsonify("Not a valid table_id"), 403
        bill = table.get_bill()
        if bill == None:
            return jsonify("Bill not created yet. try calculating it"), 403
        bill.pay()
        return jsonify("Successfully paid bill"), 200
    else:
        return jsonify("Unrecognised request", 403)
    
@app.route("/ordermanager/orders/<order_id>", methods=['GET','DELETE'])
def manage_order_by_id(order_id):
    oID = int(order_id)
    if request.method == 'GET':
        order = ordermanager.get_order(oID)
        if order == None:
            return jsonify("Not a valid order_id"), 403
        return jsonify(order.jsonify()), 200
    elif request.method == 'DELETE':
        order = ordermanager.get_order(oID)
        if order == None:
            return jsonify("Not a valid order_id"), 403
        
        tID = -1
        for i in ordermanager.map():
            if oID in ordermanager.map()[i]:
                tID = i
        
        if tID == -1:
            return jsonify("Order is not in a table. How did you manage that?"), 403
        ordermanager.remove_order(order, wms.id_to_table(tID))
        return jsonify("Successfully removed order from ordermanager"), 200

    else:
        return jsonify("Unrecognised request"), 403
    
@app.route("/ordermanager/orders/<order_id>/state", methods=['GET', 'POST'])
def affect_order_state(order_id):
    oID = int(order_id)
    if request.method == 'GET':
        order = ordermanager.get_order(oID)
        if order == None:
            return jsonify("Not a valid order_id"), 403
        output = {"state": order.state()}
        return jsonify(output), 200
    
    elif request.method == 'POST':
        '''
        EMPTY FOR NOW. WE WILL EXPAND THIS LATER TO INCLUDE STATE LEAPS IF WE WANT
        '''
        order = ordermanager.get_order(oID)
        if order == None: 
            return jsonify("Not a valid order_id", 403)
        ordermanager.change_state(oID)
        return jsonify("Successfully changed state to "+order.state()), 200

        
    else:
        return jsonify("Unrecognised request"), 403

@app.route("/ordermanager/orders/<order_id>/bill", methods=['GET', 'POST'])
def manage_order_bill(order_id):
    oID = int(order_id)
    if request.method == 'GET':
        order = ordermanager.get_order(oID)
        if order == None:
            return jsonify("Not a valid order_id"), 403
        if order.bill() == None:
            order.calculate_bill()
        output = {"price": order.bill().get_price(), "paid": order.bill().is_paid()}
        return jsonify(output), 200
    elif request.method == 'POST':
        order = ordermanager.get_order(oID)
        if order == None:
            return jsonify("Not a valid order_id"), 403
        if order.bill() == None:
            return jsonify("Order does not have a bill. Try calculating it first"), 403
        try:
            order.mark_as_paid()
        except:
            return jsonify("Order is unable to be paid at this time"), 403
        return jsonify("Bill has been paid"), 200
    else:
        return jsonify("Unrecognised request"), 403

if __name__ == '__main__':
    app.run(port=5000)