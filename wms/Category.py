from __future__ import annotations
from wms import MenuItem
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
        self.__menu_items = [] if menu_items is None else menu_items

    @property
    def id(self) -> int:
        """ Returns id """
        return self.__id
    
    @property
    def name(self) -> str:
        """ Returns name """
        return self.__name

    @property
    def menu_items(self) -> list[MenuItem]:
        """ Returns a list of menu items """
        return self.__menu_items
    
    def menu_item(self, menu_item) -> (MenuItem | None):
        """ Returns a specific menu item from category

        Args:
            menu_item (MenuItem): Menu item to be searched for

        Returns:
            MenuItem: The specific menu item from the category. None if no menu 
            item exists
        """
        # for i in self.__menu_items:
        #     if i.is_equal(menu_item):
        #         return i
        # return None
        return next((it for it in self.menu_items if it.is_equal(menu_item)), None)
    
    def menu_item_by_name(self, name) -> (MenuItem | None):
        """ Returns menu item by name

        Args:
            name (str): name of item

        Returns:
            MenuItem if present, else None 
        """
        return next((it for it in self.menu_items if it.name == name), None)

    def add_menu_item(self, menu_item) -> None:
        """ Adds a menu_item to the category

        Args:
            menu_item (MenuItem): Menu item to be added to the category

        Raises:
            ValueError: Raised if menu item is already in the category
        """
        if self.menu_item(menu_item) is not None:
            raise ValueError("Category: add_menu_item(): MenuItem already in category")
        
        self.menu_items.append(menu_item)

    def remove_menu_item(self, name) -> None:
        """ Removes a menu_item from the category

        Args:
            menu_item (MenuItem): Menu item to be removed from the category

        Raises:
            ValueError: Raised if menu item does not exist in the category
        """
        if self.menu_item_by_name(name) is None:
            raise ValueError("Category: category.remove_menu_item(): not an existing menu item")
        
        self.menu_items.remove(self.menu_item_by_name(name))
        
    def jsonify(self) -> dict:
        """ Creates a dictionary containing the id, name and list of menu items 
        of the category

        Returns:
            dict: Dictionary containing the id, name and list of menu items 
        of the category
        """

        return {
            "id": self.id, 
            "name": self.name, 
            "menu_items": [it.jsonify() for it in self.menu_items]
        }
    