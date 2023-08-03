from wms import DbHandler, Menu, Category, MenuItem, Deal, RestaurantManagerHandler
from collections import OrderedDict

class MenuHandler():
    def __init__(self, menu: Menu, db: DbHandler):
        """ Constructor for the MenuHandler Class 
        
        Args:
            menu (Menu): Menu the wait management system will show to users
            db (DbHandler): Database handler to maintain database persistence
        """
        self.__menu = menu
        self.__observers = []
        self.__db = db
    
    @property
    def menu(self) -> Menu:
        """ Returns the menu """
        return self.__menu
    
    @property
    def db(self) -> DbHandler:
        return self.__db

    def attach(self, observer: RestaurantManagerHandler):
        """ Attach observer to menu handler """
        self.__observers.append(observer)

    def notify_add(self, menu_item_id: int):
        """ Notify observers of a new addition to the menu """
        for observer in self.__observers:
            observer.menu_add(menu_item_id)

    def notify_delete(self, menu_item_id: int):
        """ Notify observers of an item deletion to the menu """
        for observer in self.__observers:
            observer.menu_delete(menu_item_id)
    
    def get_category(self, category: str) -> Category:
        """ Gets a given category from the menu

        Args:
            category (str): Category to be searched from the menu

        Returns:
            Category: Category to be acquired. Is None if category does not 
            exist
        """
        return self.__menu.get_category(category)
    
    def get_menu_item(self, category: str, name: str) -> MenuItem:
        """ Returns menu item by name

        Args:
            category (str): Category to look through 
            name (str): Name of the menu item

        Returns:
            MenuItem: MenuItem to be searched for. Is None if menu item does not 
            exist
        """
        return self.__menu.get_category(category).menu_item_by_name(name)
    
    def get_menu_item_by_id(self, id: int) -> MenuItem:
        """ Returns menu item by id

        Args:
            category (str): Category to look through 
            id (int): ID of the menu item

        Returns:
            MenuItem: MenuItem to be searched for. Is None if menu item does not 
            exist
        """
        return self.__menu.menu_item_lookup(id)
    
    def get_deals_by_id(self, id: int) -> Deal:
        """ Returns deals by id

        Args:
            id (int): ID of the deal

        Returns:
            Deal: Deal to be searched for. Is None if deal does not exist
        """
        for i in self.__menu.deals:
            if i.id == id:
                return i
        return None
    
    def add_category(self, category: str):
        """ Adds a category to the menu

        Args:
            category (str): Category to be added to the menu
        """
        self.__menu.add_category(Category(category))

    def add_menu_item(self, category: str, name: str, price: str, imageurl: str):
        """ Adds a menu item to the menu

        Args:
            category (str): Category the menu item belongs to
            name (str): Name of the menu item
            price (float): Price of the menu item
            imageurl (str): Image URL of the menu item
        """
        if self.__menu.get_category(category) is None:
            raise ValueError(f"Category with name {category} does not exist")
        
        if self.__menu.get_category(category).menu_item_by_name(name) is not None:
            raise ValueError("Menu item with this name already exists")
        item = MenuItem(name, price, imageurl)
        self.__menu.get_category(category).add_menu_item(item, self.db)
        self.notify_add(item.id)

    def add_deal(self, discount: float, menu_items: list[str]) -> None:
        """ Adds a deal to the menu

        Args:
            discount (float): Percentage discount to be applied
            menu_items (list[str]): List of menu items to be discounted by
            the deal

        Raises:
            ValueError: Raised if length of the menu items argument does not 
            match the length of the menu items to make a deal with

        Returns:
            None: Returns none if successful
        """
        deal_items = [j for i in self.__menu.categories 
                      for j in i.menu_items 
                      if j.name in menu_items]
        
        if len(menu_items) != len(deal_items):
            raise ValueError("One or more items is not present in the menu")
        
        deal = Deal(discount, deal_items)
        self.__menu.add_deal(deal, menu_items)
        return None
     
    def remove_category(self, category: str):
        """ Removes a category from the menu

        Args:
            category (str): Category to be removed
        """
        self.__menu.remove_category(category)
    
    def remove_menu_item(self, category: str, name: str):
        """ Removes a menu item from the menu

        Args:
            category (str): Category that menu item belongs to
            name (str): Name of the menu item
        """
        removed_id = self.__menu.get_category(category).remove_menu_item(name, self.db)
        self.notify_delete(removed_id)

    def update_category(self, category: str, name: str, visible: str):
        """ Updates category name and/or visibility

        Args:
            category (str): Old category name
            name (str): New category name
            visible (str): New visibility of the category in the menu

        Raises:
            ValueError: Raised if category name does not exist in the menu
        """
        curr_category = self.__menu.get_category(category)
        if curr_category is None:
            raise ValueError(f"Category {category} does not exist")
        
        if self.__menu.get_category(name) is not None:
            raise ValueError(f"Category with the name {name} already exists")
        
        curr_category.update(name, visible)

    def update_menu_item(self, category: str, old_name: str, new_name: str, 
                         price: str, image_url: str, visible: str):
        """ Updates menu item name, price, image_url and/or visibility

        Args:
            category (str): Category name the menu item is under
            old_name (str): Old name of the menu item
            new_name (str): New name of the menu item
            price (str): New price of the menu item
            image_url (str): New image url of the menu item
            visible (str): New visibiltiy of the menu item in the menu

        Raises:
            ValueError: Raised if menu item does not exist in the given category
        """
        menu_item = self.__menu.get_category(category).menu_item_by_name(old_name)
        if menu_item is None:
            raise ValueError(f"Menu Item with the name {old_name} doesn't exist in the {category} category")
        
        if self.__menu.get_category(category).menu_item_by_name(new_name) is not None:
            raise ValueError(f"Menu item with the name {new_name} already exists")
        
        menu_item.update(new_name, price, image_url, visible)

    def reorder_category(self, new_order: list[str]):
        """ Updates the order of categories in the menu

        Args:
            new_order (list[str]): List of category IDs that dictate the 
            new category order
        """                
        try:
            [int(i) for i in new_order]
        except ValueError:
            raise ValueError("New_order argument has an invalid item")
        
        self.__menu.update_categories(new_order)

    def reorder_menu_items(self, category: str, new_order: list[str]):
        """ Updates the order of menu items in a category

        Args:
            category (str): Category to have menu items reordered
            new_order (list[str]): List of menu item IDs that dictate the 
            new menu item

        Raises:
            ValueError: Raised if category does not exist in the menu
        """                
        if self.__menu.get_category(category) is None:
            raise ValueError(f"Category {category} does not exist")
        
        try:
            [int(i) for i in new_order]
        except ValueError:
            raise ValueError("New_order argument has an invalid item")
        
        self.__menu.get_category(category).update_menu_items(new_order)
        
    def search(self, query: str) -> dict:
        """ Function to perform a search with a given query string

        Args:
            query (str): Query string to use for the search

        Returns:
            dict: Dictionary filled with the search results
        """
        return self.__menu.search_items(query)

    def jsonify(self) -> dict:
        """ Creates a dictionary of the menu 

        Returns:
            dict: A dictionary of the menu 
        """
        return self.__menu.jsonify()
    
    def jsonify_category(self, category: str) -> dict:
        """ Creates a dictionary of a category of a menu

        Args:
            category (str): Category to create a dictionary out of

        Raises:
            ValueError: Raised if the category does not exist in the menu

        Returns:
            dict: A dictionary of a category of a menu
        """
        if self.__menu.get_category(category) == None:
            raise ValueError("That category doesn't exist")

        return self.__menu.get_category(category).jsonify()
    
    def jsonify_categories(self) -> dict:
        """ Creates a dictionary for all the categories of a menu

        Returns:
            dict: A dictionary for all the categories of a menu
        """
        return [i.jsonify() for i in self.__menu.categories]
    
    def jsonify_menu_item(self, category: str, name: str) -> dict:
        """ Creates a dictionary for a specific menu_item in a menu

        Args:
            category (str): Category in the menu
            name (str): Specific menu item in the category

        Raises:
            KeyError: Raised if menu item is not found in the category

        Returns:
            dict: A dictionary for a specific menu_item in a menu
        """
        try:
            menu_item = self.__menu.get_category(category).menu_item_by_name(name).jsonify()
        except:
            raise KeyError("menu_item not found")
        
        return menu_item
    
    def jsonify_deals(self) -> dict:
        """ Creates a dictionary for all the deals of a menu

        Returns:
            dict: A dictionary for all the deals of a menu
        """
        return [i.jsonify() for i in self.__menu.deals]

    def jsonify_stats(self, statistics: list[tuple]) -> dict:
        """ Converts a list with tuples of menu item ids and order frequency to 
        a dictionary with menu item names that corresponded to the ids as keys
        and frequency as values

        Args:
            statistics (list[tuple]): List of tuples of menu items ids to order
            frequency 

        Returns:
            dict: A dictionary with menu item names and frequencies as key value
            pairs
        """
        menu_item_stats = OrderedDict()
        for item in statistics:
            menu_item_stats[self.get_menu_item_by_id(item[0]).name] = item[1]

        return menu_item_stats

    def jsonify_stats_full(self, statistics: dict) -> dict:
        """ Recreates the 2D dictionary structure of full menu statistics with
        all menu item id values converted into their proper menu item names

        Args:
            statistics (dict): 2D dictionary where each key is a menu item id,
            and the key value is another dictionary relating to frequency of 
            menu items ordered with the menu item specified by the key

        Returns:
            dict: A 2D dictionary with menu item names and the number of orders
            with other menu items as key value pairs
        """
        menu_item_stats = OrderedDict()
        for key in statistics.keys():
            key_dict = {}
            for item in statistics[key]:
                key_dict[self.get_menu_item_by_id(item).name] = statistics[key][item]
            menu_item_stats[self.get_menu_item_by_id(key).name] = key_dict
        return menu_item_stats
    
    def jsonify_frequent_pairs(self, statistics: list[tuple]) -> dict:
        """ Converts a list with tuples of menu item ids and order frequency to 
        a dictionary with menu item names that corresponded to the ids as keys
        and frequency as values

        Args:
            statistics (list[tuple]): List of tuples where each tuple contains
            a menu item id and the id of the menu item that it gets ordered the
            most with

        Returns:
            dict: A dictionary with a menu item as a key and the its most 
            frequent menu item pairing as its key value
        """
        menu_item_stats = OrderedDict()
        for item in statistics:
            item_1 = self.get_menu_item_by_id(item[1])
            item_1_name = item_1.name if item_1 is not None else "None"
            menu_item_stats[self.get_menu_item_by_id(item[0]).name] = item_1_name

        return menu_item_stats
