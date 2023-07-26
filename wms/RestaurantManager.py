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
            self.statistics[menu_item_id] = {}
            for key in self.statistics.keys():
                self.statistics[key][menu_item_id] = 0
                self.statistics[menu_item_id][key] = 0
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
            for key in self.statistics.keys():
                if menu_item_id in self.statistics[key]:
                    self.statistics[key].pop(menu_item_id)
            self.statistics.pop(menu_item_id)
        else:
            raise ValueError("RestaurantManager: delete_menu_item(): Menu Item is not in the statistics")
        
    def increase_count(self, menu_items: list[int]):
        """ Increments count of a menu item key in the dictionary for tracking
        menu item frequency. When there are multiple items in the order it 
        updates the 2D dictionary structure accordingly

        Args:
            menu_items (list[Integer]): List of menu items ordered

        Raises:
            ValueError: Raised if a menu item is not in the dictionary
        """
        for item in menu_items:
            if item not in self.statistics:
                raise ValueError("RestaurantManager: increase_count(): Menu Item is not in the statistics")
            self.statistics[item][item] += 1
            
        sorted_menu_items = sorted(menu_items)
        for i in range(len(sorted_menu_items) - 1):
            key = sorted_menu_items[i]
            rest = sorted_menu_items[i + 1:]
            for item in rest:
                if key is not item:
                    self.statistics[key][item] += 1
                    self.statistics[item][key] += 1

    def jsonify(self, reverse = True) -> list:
        """ Creates a list of all the menu items and the number of menu item 
        orders. Used when sorting most and least popular menu items

        Args:
            reverse (bool, optional): Boolean to sort by ascending or descending
            frequency. Defaults to True.

        Returns:
            list: A list of all the menu items and the number of menu item 
        orders
        """
        new_list = [(i[0], i[1][i[0]]) for i in self.statistics.items()]
        return sorted(new_list, key=lambda item:item[1], reverse=reverse)

    def jsonify_full(self) -> dict:
        """ Returns entire 2D structure of menu statistics

        Returns:
            Dict: A dictionary where each key corresponds to a menu item with a
            dictionary of its frequency of orders with other menu items as the
            key value 
        """
        return self.statistics
    
    def jsonify_frequent_pair(self) -> list[tuple]:
        """ Returns the most paired item for each menu item

        Returns:
            List[Tuple]: List of tuples where each tuple contains the menu item
            id and its most paired menu item's id 
        """
        frequent_pairs = []
        for item in self.statistics.items():
            menu_item_frequencies = item[1].items()
            sorted_list = sorted(menu_item_frequencies, key=lambda num:num[1], reverse=True)
            top_pairing = sorted_list[0] if sorted_list[0][0] != item[0] else sorted_list[1]
            frequent_pairs.append((item[0], top_pairing[0]))
        return frequent_pairs
            