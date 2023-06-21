from .Category import Category
from .MenuItem import MenuItem
from .Deal import Deal

class Menu():

    def __init__(self, categories=None, deals=None):

        self.__categories = categories
        self.__deals      = deals

        if self.__categories == None:
            self.__categories = []
        
        if self.__deals == None:
            self.__deals = []

    # Returns a list of categories 
    def categories(self):
        return self.__categories
    
    # Returns a list of deals
    def deals(self):
        return self.__deals
    

    # Returns a category with a matching name attribute
    def get_category(self, name):
        for i in self.__categories:
            if i.name() == name:
                return i
        return None

    # Adds a new category to the menu
    def add_category(self, category):
        if not isinstance(category, Category):
            raise TypeError("Menu: add_category(): Object is not of type Category")
        
        if category in self.__categories:
            raise ValueError("Menu: add_category(): Category already exists")

        self.__categories.append(category)


    # Removes a category, if that category exists, from the menu.
    # Returns the removed category
    def remove_category(self, name):

        if not isinstance(name, str):
            raise TypeError("Menu: menu.remove_category(): not a string")
        for i in self.__categories:
            if i.name() == name:
                self.__categories.remove(i)
                return i
        
        raise ValueError("Menu: menu.remove_category(): not in categories")
    
    # Adds a new deal to the menu
    def add_deal(self, deal):
        if not isinstance(deal, Deal):
            raise TypeError("Menu: add_deal(): Object is not of type Deal")
        
        if deal in self.__deals:
            raise ValueError("Menu: add_deal(): Deal already exists")
        
        self.__deals.append(deal)
    
    # Removes a deal from the menu.
    # Returns removed deal
    def remove_deal(self, deal):
        if not isinstance(deal, Deal):
            raise TypeError("Menu: menu.remove_deal(): Object is not of type Deal")
        
        if deal not in self.__deals:
            raise ValueError("Menu: menu.remove_deal(): not in deals")
        
        self.__deals.remove(deal)
        return deal

        
