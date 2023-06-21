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
    
    # Returns a specific menu item from category
    # Returns None if no menu item exists
    def menu_item(self, name):
        for i in self.__menu_items:
            if i.name() == name:
                return i
        return None
    
    # Changes the name of the category


    # Adds a menu_item to the category
    def add_menu_item(self, menu_item):
        if not isinstance(menu_item, MenuItem):
            raise TypeError("Category: add_menu_item(): Object not of type MenuItem")
        
        if menu_item in self.__menu_items:
            raise ValueError("Category: add_menu_item(): MenuItem already in category")
        
        self.__menu_items.append(menu_item)

    # Removes a menu_item from the category
    def remove_menu_item(self, menu_item):
        if not isinstance(menu_item, MenuItem):
            raise TypeError("Category: category.remove_menu_item(): Object is not of type MenuItem")
        
        if menu_item not in self.__menu_items:
            raise ValueError("Category: category.remove_menu_item(): not an existing menu item")
        
        self.__menu_items.remove(menu_item)
        return menu_item


        
