from flask import Flask, jsonify, request, current_app
from wms import *
import json

app = Flask(__name__)

wms = Application()

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
                return "Incorrect fields"
            
            wms.add_menu_item(category, name, price, imageURL)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)