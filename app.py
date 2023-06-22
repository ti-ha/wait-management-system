from flask import Flask, jsonify, request
from wms import *
import json

app = Flask(__name__)

menu = Menu()

# A lot of the logic in here needs to be refactored to a new class. Speedrunning for now to get API working for frontend

@app.route('/')
def home():
    return "Hello world!"

@app.route('/menu', methods=['GET'])
def get_menu():
    return menu.jsonify()

@app.route('/menu/categories', methods=['GET','POST'])
def create_category():
    if request.method == "GET":
        categories = menu.categories()
        output = [i.jsonify() for i in categories]
        return output
    elif request.method == "POST":
        '''
        JSON FORMAT:
        {"name": "string"}
        '''
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            obj = request.json
            menu.add_category(Category(obj["name"]))
            return ("Successfully added category " + obj["name"])
        else:
            return "Incorrect content-type"

@app.route('/menu/categories/<category>', methods=['GET', 'POST', 'DELETE'])
def specific_category(category):
    cat = menu.get_category(category)
    if request.method == 'GET':
        return cat.jsonify()
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
            
            menu_item = MenuItem(name, price)
            cat.add_menu_item(menu_item)
            return ("Successfully added menuitem " + obj["name"])
        
    elif request.method == 'DELETE':
        '''
        REMOVING A SPECIFIC CATEGORY. DELETE METHOD FOR MENUITEM
        IS IN THE SPECIFIC ROUTE FOR SPECIFIC MENU ITEM
        '''
        menu.remove_category(category)
        return ("Successfully deleted category" + category)

    else:
        return "Not a valid request"
    
@app.route('/menu/categories/<category>/<menu_item>', methods=['GET', 'DELETE'])
def menu_item(category, menu_item):
    item = menu.get_category(category).menu_item(menu_item)

    if item == None:
        return "Unrecognised menu_item"
    
    if request.method == 'GET':
        return item.jsonify()
        
    elif request.method == 'DELETE':
        menu.get_category(category).remove_menu_item(item)
        return "Successfully removed menuitem "+menu_item+" in category "+category
    else:
        return "Unrecognised request"

@app.route('/menu/deals', methods=['GET','POST'])
def create_deal():
    if request.method == 'GET':
        deals = menu.deals()
        output = [i.jsonify() for i in deals]
        return output
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
            
            deal_items = []
            for i in menu.categories():
                for j in i.menu_items():
                    if j.name() in menu_item_lookup:
                        deal_items.append(j)
            
            if len(menu_item_lookup) != len(deal_items):
                return "One or more menu items does not exist"
            deal = Deal(obj["discount"], deal_items)
            menu.add_deal(deal)

            return ("Successfully added deal with new id "+str(deal.id()))
        
        else:
            return "Incorrect content-type"
    else:
        return "Unrecognised request"

if __name__ == '__main__':
    app.run(port=5000)