from wms import (
    RestaurantManager, TableHandler, UserHandler, Table, User, WaitStaff, 
    KitchenStaff, Manager
)
from functools import cmp_to_key

class RestaurantManagerHandler():
    def __init__(self, restaurant_manager, menu_handler, order_handler, table_handler, user_handler):
        """ Constructor for the RestaurantManagerHandler Class """
        self.__rm = restaurant_manager
        self.__table_handler = table_handler
        self.__user_handler = user_handler

        self.__menu_handler = menu_handler
        self.__order_handler = order_handler
        self.__menu_handler.attach(self)
        self.__order_handler.attach(self)

    @property
    def rm(self) -> RestaurantManager:
        """ Returns the ServiceRequestManager object """
        return self.__rm
    
    @property
    def table_handler(self) -> TableHandler:
        """ Returns the User Handler object """
        return self.__table_handler
    
    @property
    def user_handler(self) -> UserHandler:
        """ Returns the User Handler object """
        return self.__user_handler

    def menu_add(self, menu_item_id: int):
        """ Adds a statistic dictionary key """
        self.rm.add_menu_item(menu_item_id)

    def menu_delete(self, menu_item_id: int):
        """ Removes a statistic dictionary key """
        self.rm.delete_menu_item(menu_item_id)

    def order_update(self, menu_items: list[int]):
        """ Update statistic dictionary values """
        self.rm.increase_count(menu_items)

    def get_menu_stats(self):
        return self.__menu_handler.jsonify_stats(self.rm.jsonify())

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

        Args:
            table_list (list[Table]): List of tables to jsonify

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

        Args:
            table_list (list[Table]): List of tables to jsonify

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
    
    def staff_sort_position(self) -> dict:
        """ Sorts the staff members by their position

        Returns:
            Dict: A dictionary containing information about all the staff 
            members sorted by their position
        """
        staff_list = [i for i in self.user_handler.users if i.__class__ in [WaitStaff, KitchenStaff, Manager]]
        sorted_list = sorted(staff_list, key=lambda user: len(user.__class__.__name__))
        return self.jsonify_user_position(sorted_list)
    
    def staff_sort_status(self) -> dict:
        """ Sorts the staff members by their login status

        Returns:
            Dict: A dictionary containing information about all the staff 
            members sorted by their login status
        """
        staff_list = [i for i in self.user_handler.users if i.__class__ in [WaitStaff, KitchenStaff, Manager]]
        sorted_list = sorted(staff_list, key=lambda user: (not user.status, len(user.__class__.__name__)))
        return self.jsonify_user_status(sorted_list)
    
    def jsonify_user_position(self, user_list: list[User]) -> dict:
        """ Creates a dictionary containing the id, first name, last name and
        position of the staff member.

        Args:
            user_list (list[User]): List of users to jsonify

        Returns:
            Dict: A dictionary containing the id, first name, last name and
        position of the staff member.
        """
        user_info = []
        for user in user_list:
            user_dict = user.jsonify()
            user_dict.pop("password")
            user_info.append(user_dict)
        return {"staff": user_info}
    
    def jsonify_user_status(self, user_list: list[User]) -> dict:
        """ Creates a dictionary containing the id, first name, last name,
        position and login status of the staff member.

        Args:
            user_list (list[User]): List of users to jsonify

        Returns:
            Dict: A dictionary containing the id, first name, last name and
        position of the staff member.
        """
        user_info = []
        for user in user_list:
            user_dict = user.jsonify()
            user_dict.pop("password")
            user_dict["logged in"] = user.status
            user_info.append(user_dict)
        return {"staff": user_info}