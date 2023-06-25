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

if __name__ == '__main__':
    app.run(port=5000)