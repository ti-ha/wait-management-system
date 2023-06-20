from .MenuItem import MenuItem
import itertools

class Deal():

    # Primary key
    __id_iter = itertools.count()

    def __init__(self, discount, menu_items=None):
        self.__id = next(Deal.__id_iter)
        self.__discount = float(discount)
        self.__menu_items = menu_items
        # getting around annoying python default value behaviour
        if self.__menu_items is None:
            self.__menu_items = []

    # Returns the unique id of the deal.
    def id(self):
        return self.__id
    
    # Returns the discount
    def discount(self):
        return self.__discount
    
    # Returns all menu items associated with the deal
    def menu_items(self):
        return self.__menu_items
    
    # Adds a menu item to the deal.
    def add_menu_item(self, menu_item):
        if not isinstance(menu_item, MenuItem):
            raise TypeError("Deal: add_menu_item(): Object not of type MenuItem")
        
        if menu_item in self.__menu_items:
            raise ValueError("Deal: add_menu_item(): MenuItem already in category")
        
        self.__menu_items.append(menu_item)
    
    # Removes a menu item to the deal.
    # Returns the deleted menu item
    def remove_menu_item(self, menu_item):
        if not isinstance(menu_item, MenuItem):
            raise TypeError("Deal: category.remove_menu_item(): Object is not of type MenuItem")
        
        if menu_item not in self.__menu_items:
            raise ValueError("Deal: category.remove_menu_item(): not a menu item")
        
        self.__menu_items.remove(menu_item)
        return menu_item
    
    # Sets the discount.
    def set_discount(self, discount):
        if self.isfloat(discount):
            self.__discount = float(discount)
        
        return ValueError("Deal: deal.set_discount(num): num is not floatable")

    
    # Checks if the deal is applicable to a specific menu_item.
    def is_applicable(self, menu_item):
        if not isinstance(menu_item, MenuItem):
            raise TypeError("Deal: deal.is_applicable(): Object is not of type MenuItem")
        
        if menu_item in self.__menu_items:
            return True
        
        return False
    
    # Helper function for parsing input
    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False
