from __future__ import annotations
from .MenuItem import MenuItem
import itertools

class Deal():

    # Primary key
    __id_iter = itertools.count()

    def __init__(self, discount, menu_items=None):
        """ Constructor for the Deal Class

        Args:
            discount (float): Discount percentage that applies to the deal
            menu_items (MenuItem, optional): Menu items that the deal applies
            to. Defaults to None.
        """
        self.__id = next(Deal.__id_iter)
        # A float value between 0 and 1 (percentage discount)
        self.__discount = float(discount)
        self.__menu_items = menu_items
        # getting around annoying python default value behaviour

        # We need this for when someone passes only one menu item into the deal so it still ends up as an array.
        # Not sure where else this is a problem
        if isinstance(menu_items, MenuItem):
            self.__menu_items = [menu_items]
        else:
            self.__menu_items = menu_items

        self.__menu_items = [] if menu_items == None else menu_items

    @property
    def id(self):
        """ Returns the unique id of the deal """
        return self.__id
    
    @property
    def discount(self):
        """ Returns the discount """
        return self.__discount
    
    @discount.setter
    def discount(self, discount):
        """ Sets the discount for the deal """
        if Deal.isfloat(discount):
            self.__discount = float(discount)
            return
        else:
            raise ValueError("Deal: deal.set_discount(num): num is not floatable")
        
    @property
    def menu_items(self) -> list[MenuItem]:
        """ Returns all menu items associated with the deal """
        return self.__menu_items
    
    @property
    def visible(self) -> bool:
        """ Returns if the deal should be visible based on the menu-items in the
        deal"""
        return next((i for i in self.menu_items if i.visible == False), None) == None
    
    def add_menu_item(self, menu_item):
        """ Adds a menu item to the deal.

        Args:
            menu_item (MenuItem): Menu item that will be discounted by the deal

        Raises:
            TypeError: Raised when menu_item argument is not of type MenuItem
            ValueError: Raised when menu_item is already apart of this deal
        """
        if not isinstance(menu_item, MenuItem):
            raise TypeError("Deal: add_menu_item(): Object not of type MenuItem")
        
        if menu_item in self.__menu_items:
            raise ValueError("Deal: add_menu_item(): MenuItem already in deal")
        
        self.__menu_items.append(menu_item)

    def remove_menu_item(self, menu_item) -> MenuItem:
        """ Removes a menu item to the deal.

        Args:
            menu_item (MenuItem): Menu Item to remove from the deal

        Raises:
            TypeError: Raised when menu_item argument is not of type MenuItem
            ValueError: Raised when menu_item is not apart of this deal

        Returns:
            MenuItem: Returns the removed menu item
        """
        if not isinstance(menu_item, MenuItem):
            raise TypeError("Deal: category.remove_menu_item(): Object is not of type MenuItem")
        
        if menu_item not in self.__menu_items:
            raise ValueError("Deal: category.remove_menu_item(): not a menu item")
        
        self.__menu_items.remove(menu_item)
        return menu_item
    
    def is_applicable(self, menu_item) -> bool:
        """ Checks if the deal is applicable to a specific menu_item.

        Args:
            menu_item (MenuItem): Menu Item to be checked

        Raises:
            TypeError: Raised when menu_item argument is not of type MenuItem

        Returns:
            Boolean: Returns true if menu_item is discounted by this deal, false
            otherwise
        """
        if not isinstance(menu_item, MenuItem):
            raise TypeError("Deal: deal.is_applicable(): Object is not of type MenuItem")
        
        if menu_item in self.__menu_items:
            return True
        
        return False
    
    def isfloat(num) -> bool:
        """ Helper function for parsing input

        Args:
            num (any): Argument to check if it is of type float

        Returns:
            Boolean: True if argument is of type float, false otherwise
        """
        try:
            float(num)
            return True
        except ValueError:
            return False
        
    def jsonify(self) -> dict:
        """ Creates a dictionary containing the id and discount value of the 
        deal

        Returns:
            dict: Dictionary containing the id and discount value of the deal
        """
        return {
            "id": self.id, 
            "discount": self.discount, 
            "menu_items": [{"id": i.jsonify()["id"], 
                            "name": i.jsonify()["name"], 
                            "price": round(i.jsonify()["price"] - i.jsonify()["price"]*self.discount, 2),
                            "imageURL": i.jsonify()["imageURL"],
                            "visible": i.jsonify()["visible"]} for i in self.menu_items]
            }
