from __future__ import annotations
from .Category import Category
from .MenuItem import MenuItem
from .Deal import Deal

class Menu():

    def __init__(self, categories=None, deals=None):
        """ Constructor for the Menu class

        Args:
            categories (List[Category], optional): Different menu categories. 
            Defaults to None.
            deals (List[Deal], optional): Different menu deals. 
            Defaults to None.
        """
        self.__categories = [] if categories == None else categories
        self.__deals = [] if deals == None else deals
 
    @property
    def categories(self) -> list[Category]:
        """ Returns a list of categories """
        return self.__categories
    
    @property
    def deals(self) -> list[Deal]:
        """ Returns a list of deals """
        return self.__deals
    
    def get_category(self, name):
        """ Returns a category with a matching name attribute

        Args:
            name (string): Name of the category 

        Returns:
            Category: Category to be acquired. If no category is found returns
            None
        """
        for i in self.__categories:
            if i.name == name:
                return i
        return None

    def add_category(self, category):
        """ Adds a new category to the menu

        Args:
            category (Category): Category to be added to the menu

        Raises:
            TypeError: Raised if category argument is not of type category
            ValueError: Raised if category already exists in the menu
        """
        if not isinstance(category, Category):
            raise TypeError("Menu: add_category(): Object is not of type Category")
        
        if category in self.__categories:
            raise ValueError("Menu: add_category(): Category already exists")

        self.__categories.append(category)

    def remove_category(self, name):
        """ Removes a category, if that category exists, from the menu.

        Args:
            name (string): Name of the category to be removed

        Raises:
            TypeError: Raised if name argument is not a string
            ValueError: Raised if category does not exist in the menu

        Returns:
            Category: Returns the removed category
        """
        if not isinstance(name, str):
            raise TypeError("Menu: menu.remove_category(): not a string")
        for i in self.__categories:
            if i.name() == name:
                self.__categories.remove(i)
                return i
        
        raise ValueError("Menu: menu.remove_category(): not in categories")
    
    def add_deal(self, deal):
        """ Adds a new deal to the menu

        Args:
            deal (Deal): Deal to be added to the menu

        Raises:
            TypeError: Raised if deal object is not of type Deal
            ValueError: Raised if deal already exists in the menu
        """
        if not isinstance(deal, Deal):
            raise TypeError("Menu: add_deal(): Object is not of type Deal")
        
        if deal in self.__deals:
            raise ValueError("Menu: add_deal(): Deal already exists")
        
        self.__deals.append(deal)
    
    def remove_deal(self, deal):
        """ Removes a deal from the menu.

        Args:
            deal (Deal): Deal to be removed from the menu

        Raises:
             TypeError: Raised if deal object is not of type Deal
            ValueError: Raised if deal does not exist in the menu

        Returns:
            Deal: Returns removed deal
        """
        if not isinstance(deal, Deal):
            raise TypeError("Menu: menu.remove_deal(): Object is not of type Deal")
        
        if deal not in self.__deals:
            raise ValueError("Menu: menu.remove_deal(): not in deals")
        
        self.__deals.remove(deal)
        return deal
    
    def menu_items(self) -> list[MenuItem]:
        """ Returns a list of menu items

        Returns:
            list[MenuItem]: List of menu items in menu
        """
        output = []
        for i in self.categories:
            output += i.menu_items
        return output
    
    def menu_item_lookup(self, id) -> MenuItem:
        """ Performs a look up through the menu's menu items

        Args:
            id (integer): ID of menu item to be searched for

        Returns:
            MenuItem: Menu item to be searched for if found. Returs None if 
            menu item cannot be found.
        """
        for i in self.menu_items():
            if i.id == id:
                return i
        return None
    
    def jsonify(self) -> dict:
        """ Creates a dictionary containing the categories and deals of the 
        menu

        Returns:
            dict: Dictionary containing the categories and deals of the menu
        """
        output = {'categories': [], 'deals': []}
        for i in self.categories:
            output['categories'].append(i.jsonify())
        for j in self.deals:
            output['deals'].append(j.jsonify())
        
        return output

        
