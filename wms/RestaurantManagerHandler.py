from wms import RestaurantManager, MenuHandler, TableHandler, UserHandler, Table
from Order import State
from functools import cmp_to_key

class RestaurantManagerHandler():
    def __init__(self, restaurant_manager, menu_handler, table_handler, user_handler):
        """ Constructor for the RestaurantManagerHandler Class """
        self.__rm = restaurant_manager
        self.__menu_handler = menu_handler
        self.__table_handler = table_handler
        self.__user_handler = user_handler

    @property
    def rm(self) -> RestaurantManager:
        """ Returns the ServiceRequestManager object """
        return self.__rm
    
    @property
    def menu_handler(self) -> MenuHandler:
        """ Returns the User Handler object """
        return self.__menu_handler
    
    @property
    def table_handler(self) -> TableHandler:
        """ Returns the User Handler object """
        return self.__table_handler
    
    @property
    def user_handler(self) -> UserHandler:
        """ Returns the User Handler object """
        return self.__user_handler
    
    def tables_sort_size(self) -> dict:
        """ Sorts the tables by their table size

        Returns:
            Dict: A dictionary containing information about all the tables
            sorted by their table size
        """
        sorted_list = sorted(self.table_handler.tables, key=lambda table: table.table_limit)
        return self.table_handler.jsonify(sorted_list)
    
    def tables_sort_orders(self) -> dict:
        """ Sorts the tables by their order status

        Returns:
            Dict: A dictionary containing information about all the tables
            sorted by their order status
        """
        sorted_list = sorted(self.table_handler.tables, key=cmp_to_key(self.table_order_compare))
        return self.table_handler.jsonify(sorted_list)

    def table_order_compare(table_1: Table, table_2: Table) -> int:
        """ Compare function to compare two tables by their order status

        Args:
            table_1 (Table): First table
            table_2 (Table): Second table to be compared to the first table

        Returns:
            int: Integer representing the difference in order status between 
            two tables
        """
        return sum([i.state_value for i in table_1.orders]) - sum([i.state_value for i in table_2.orders])
    
   