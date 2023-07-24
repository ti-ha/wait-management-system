class RestaurantManager:
    def __init__(self):
        """ Constructor for the RestaurantManager Class """
        self.__statistics = {}

    @property
    def statistics(self) -> dict:
        """ Returns statistics list """
        return self.__statistics

    def add_menu_item(self, menu_item_id: int):
        """ Adds menu item id to statistics dictionary

        Args:
            menu_item_id (Integer): Menu item to be added to the dictionary

        Raises:
            ValueError: Raised if menu item is already in the dictionary
        """
        if menu_item_id not in self.statistics:
            self.statistics[menu_item_id] = 0
        else:
            raise ValueError("RestaurantManager: add_menu_item(): Menu Item is already in the statistics")
        
    def delete_menu_item(self, menu_item_id: int):
        """ Deletes a menu item id to statistics dictionary

        Args:
            menu_item_id (Integer): Menu item to be removed from the dictionary

        Raises:
            ValueError: Raised if menu item is not in the dictionary
        """
        if menu_item_id in self.statistics:
            self.statistics.pop(menu_item_id)
        else:
            raise ValueError("RestaurantManager: delete_menu_item(): Menu Item is not in the statistics")
        
    def increase_count(self, menu_items: list[int]):
        """ Increments count of a menu item key in the dictionary for tracking
        menu item frequency

        Args:
            menu_items (list[Integer]): List of menu items ordered

        Raises:
            ValueError: Raised if a menu item is not in the dictionary
        """
        for item in menu_items:
            if item not in self.statistics:
                raise ValueError("RestaurantManager: increase_count(): Menu Item is not in the statistics")
            self.statistics[item] += 1

    def jsonify(self, reverse = True) -> list:
        """ Creates a list of all the menu items and the number of menu item 
        orders

        Args:
            reverse (bool, optional): Boolean to sort by ascending or descending
            frequency. Defaults to True.

        Returns:
            list: A list of all the menu items and the number of menu item 
        orders
        """
        return sorted(self.statistics.items(), key=lambda item:item[1], reverse=reverse)