from wms import RestaurantManager, MenuHandler, TableHandler, UserHandler, Table
from wms.Order import State
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
        return self.jsonify_tables_size(sorted_list)
    
    def tables_sort_orders(self) -> dict:
        """ Sorts the tables by their order status

        Returns:
            Dict: A dictionary containing information about all the tables
            sorted by their order status
        """
        sorted_list = sorted(self.table_handler.tables, key=cmp_to_key(self.table_order_compare))
        return self.jsonify_tables_orders(sorted_list)

    def table_order_compare(self, table_1: Table, table_2: Table) -> int:
        """ Compare function to compare two tables by their order status

        Args:
            table_1 (Table): First table
            table_2 (Table): Second table to be compared to the first table

        Returns:
            int: Integer representing the difference in order status between 
            two tables
        """
        table_1_orders = self.get_min_order_state(table_1)[0]
        table_2_orders = self.get_min_order_state(table_2)[0]
        return table_1_orders - table_2_orders
    
    def get_min_order_state(self, table: Table) -> list:
        """ Get the lowest order status of the table with its corresponding 
        order id

        Args:
            table (Table): Table that contains the list of orders to go through

        Returns:
            tuple: Contains the lowest order status and its corresponding order
            id
        """
        order_states = [[i.state_value, i.state, i.id] for i in table.orders if i.state_value != -1]
        sorted_states = sorted(order_states, key=lambda value: value[0])
        return sorted_states[0]
    
    def jsonify_tables_size(self, table_list : list[Table]) -> dict:
        """ Creates a dictionary containing the id, availability string, table
        limit and occupied boolean of the table that have been sorted by table 
        limit 

        Returns:
            Dict: A dictionary containing the id, availability string, table
        limit and occupied boolean of the table that have been sorted by table
        limit
        """
        return {"tables": [table.jsonify() for table in table_list]}
    
    def jsonify_tables_orders(self, table_list : list[Table]) -> dict:
        """ Creates a dictionary containing the id, availability string, table
        limit, occupied boolean and the state and order_id of lowest order
        status of the table (ignoring deleted orders)

        Returns:
            Dict: A dictionary containing the id, availability string, table
        limit, occupied boolean and the state and order_id of lowest order
        status of the table (ignoring deleted orders)
        """
        table_info = []
        for table in table_list:
            table_dict = table.jsonify()
            table_dict["state"] = self.get_min_order_state(table)[1]
            table_dict["order_id"] = self.get_min_order_state(table)[2]
            table_info.append(table_dict)
        return {"tables": table_info}