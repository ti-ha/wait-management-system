from flask import Blueprint
from wms import *
from middlewares import backend, token_optional, token_required, call
from flask import request, jsonify

menu_blueprint = Blueprint('menu', __name__)

@menu_blueprint.route('/menu', methods=['GET'], endpoint='get_menu')
def get_menu():
    """ Gets the restaurant menu """

    return call(
        None, 
        backend.menu_handler.jsonify
    )

@menu_blueprint.route('/menu/categories', methods=['GET'], endpoint='get_categories')
def get_categories():
    """ Gets the menu categories """
    return call(
        None, 
        backend.menu_handler.jsonify_categories
    )

@menu_blueprint.route('/menu/categories', methods=['POST'], endpoint='create_category')
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
        backend.menu_handler.add_category,
        obj["name"]
    )

@menu_blueprint.route('/menu/categories/<category>', methods=['GET'])
def get_category(category):
    """ Gets a specific menu category """
    return call(
        None, 
        backend.menu_handler.jsonify_category, 
        category
    )

@menu_blueprint.route('/menu/categories/<category>', methods=['PATCH'], endpoint='update_category')
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
            backend.menu_handler.update_category,
            category,
            new_name,
            visible
        )

@menu_blueprint.route('/menu/categories/order', methods=['POST'], endpoint='reorder_categories')
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
            backend.menu_handler.reorder_category,
            new_order
        )
    return None

@menu_blueprint.route('/menu/categories/<category>', methods=['POST'], endpoint='add_menu_item_to_category')
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
            backend.menu_handler.add_menu_item,
            category,
            name,
            price,
            image_url
        )
    return None

@menu_blueprint.route('/menu/categories/<category>', methods=['DELETE'], endpoint='delete_category')
@token_required
def delete_category(current_user, category):
    """ Removes a specific category """

    if current_user.__class__ is not Manager:
        return jsonify({"error": "Must be Manager to make this request"}), 401

    return call(
        {"message": f"Successfully deleted category {category}"},
        backend.menu_handler.remove_category,
        category
    )

@menu_blueprint.route('/menu/categories/<category>/order', methods=['POST'], endpoint='reorder_menu_items')
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
            backend.menu_handler.reorder_menu_items,
            category,
            new_order
        )
    return None

@menu_blueprint.route('/menu/categories/<category>/<menu_item>', methods=['GET'], endpoint='get_menu_item')
def get_menu_item(category, menu_item):
    """ Gets a specific menu item from a specific category """
    return call(
        None, 
        backend.menu_handler.jsonify_menu_item, 
        category, 
        menu_item)

@menu_blueprint.route('/menu/categories/<category>/<menu_item>', methods=['DELETE'], endpoint='delete_menu_item')
@token_required
def delete_menu_item(current_user, category, menu_item):
    """ Removes a specific menu item from a specific category """
    if current_user.__class__ is not Manager:
        return jsonify({"error": "Must be Manager to make this request"}), 401

    return call(
        {"message": f"Successfully removed menuitem {menu_item} in category {category}"},
        backend.menu_handler.remove_menu_item,
        category,
        menu_item
    )

@menu_blueprint.route('/menu/categories/<category>/<menu_item>', methods=['PATCH'], endpoint='update_menu_item')
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
            backend.menu_handler.update_menu_item,
            category,
            menu_item,
            new_name,
            price,
            image_url,
            visible
        )

@menu_blueprint.route('/menu/deals', methods=['GET'], endpoint='get_deal')
def get_deal():
    """ Gets a menu deal """
    return call(
        None, 
        backend.menu_handler.jsonify_deals
    )

@menu_blueprint.route('/menu/deals', methods=['POST'], endpoint='create_deal')
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
            backend.menu_handler.add_deal,
            obj["discount"],
            menu_item_lookup
        )
    return jsonify({"error": "Incorrect content-type"}), 400

@menu_blueprint.route('/menu/search', methods=['GET'], endpoint='search_menu')
def search_menu():
    query = request.args.get('query')

    return call(
        None, 
        backend.menu_handler.search,
        query
    )
