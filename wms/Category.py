from __future__ import annotations
from .MenuItem import MenuItem
import itertools

class Category():

    __id_iter = itertools.count()

    def __init__(self, name, menu_items=None):
        """ Constructor (no menu items by default)

        Args:
            name (string): Name of the category
            menu_items (List[MenuItem], optional): List of menu items to be 
            predefined with the new category. Defaults to None.
        """
        self.__id = next(Category.__id_iter)
        self.__name = name
        self.__menu_items = [] if menu_items == None else menu_items

    # Getters
    def get_id(self) -> itertools.count:
        return self.__id
    
    # Returns name of category
    def name(self) -> str:
        return self.__name

    # Returns list of menu items
    def get_menu_items(self) -> list[MenuItem]:
        return self.__menu_items
    
    def is_menu_item(self, menu_item) -> MenuItem:
        """ Returns a specific menu item from category

        Args:
            menu_item (MenuItem): Menu item to be searched for

        Returns:
            MenuItem: The specific menu item from the category. None if no menu 
            item exists
        """
        for i in self.__menu_items:
            if i.is_equal(menu_item):
                return i
        return None
    
    def get_menu_item_by_name(self, name):
        for i in self.__menu_items:
            if i.name() == name:
                return i
        return None
    
    # Changes the name of the category

    def add_menu_item(self, menu_item):
        """ Adds a menu_item to the category

        Args:
            menu_item (MenuItem): Menu item to be added to the category

        Raises:
            ValueError: Raised if menu item is already in the category
        """
        if self.is_menu_item(menu_item) != None:
            raise ValueError("Category: add_menu_item(): MenuItem already in category")
        
        self.__menu_items.append(menu_item)

    def remove_menu_item(self, name):
        """ Removes a menu_item from the category

        Args:
            menu_item (MenuItem): Menu item to be removed from the category

        Raises:
            ValueError: Raised if menu item does not exist in the category
        """
        if self.is_menu_item(name) == None:
            raise ValueError("Category: category.remove_menu_item(): not an existing menu item")
        
        self.__menu_items.remove(name)
    
    def jsonify(self) -> dict:
        """ Creates a dictionary containing the id, name and list of menu items 
        of the category

        Returns:
            dict: Dictionary containing the id, name and list of menu items 
        of the category
        """
        out = {"id": self.get_id(), "name": self.name(), "menu_items": []}
        for i in self.get_menu_items():
            out["menu_items"].append(i.jsonify())
        return out
    


        
