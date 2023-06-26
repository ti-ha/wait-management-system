from .MenuItem import MenuItem
import itertools

class Category():

    __id_iter = itertools.count()

    # Constructor (no menu items by default)
    def __init__(self, name, menu_items=None):
        self.__id = next(Category.__id_iter)
        self.__name = name
        self.__menu_items = menu_items
        if self.__menu_items is None:
            self.__menu_items = []

    def id(self):
        return self.__id
    
    # Returns name of category
    def name(self):
        return self.__name

    # Returns list of menu items
    def menu_items(self):
        return self.__menu_items
    
    def get_menu_items(self):
        return self.__menu_items
    
    # Returns a specific menu item from category
    # Returns None if no menu item exists
    def is_menu_item(self, menu_item):
        for i in self.__menu_items:
            if i.is_equal(menu_item):
                return i
        return None
    
    # Changes the name of the category


    # Adds a menu_item to the category
    def add_menu_item(self, menu_item):
        if self.is_menu_item(menu_item) != None:
            raise ValueError("Category: add_menu_item(): MenuItem already in category")
        
        self.__menu_items.append(menu_item)

    # Removes a menu_item from the category
    def remove_menu_item(self, name):
        if self.is_menu_item(name) == None:
            raise ValueError("Category: category.remove_menu_item(): not an existing menu item")
        
        self.__menu_items.remove(name)
    
    def jsonify(self):
        out = {"id": self.id(), "name": self.name(), "menu_items": []}
        for i in self.menu_items():
            out["menu_items"].append(i.jsonify())
        return out
    


        
