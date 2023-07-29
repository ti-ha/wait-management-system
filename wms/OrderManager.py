from __future__ import annotations
from wms import Table, Bill, States
from .Order import Order

class OrderManager:
    def __init__(self):
        """ Constructor for the Order Manager class """
        self.__orders = []

        # Contains all previous orders including those completed and deleted
        self.__history = []

        # maps table: [orders]
        self.__map = {}
        
    # Getter
    @property
    def orders(self) -> list[Order]:
        """ Returns list of orders """
        return self.__orders
    
    @property
    def history(self) -> list[Order]:
        """ Returns order history"""
        return self.__history
    
    @property
    def map(self) -> dict:
        """ Returns dictionary linking tables to list of orders """
        return self.__map
    
    def get_order(self, order_id) -> Order:
        """ Returns a specific order based off provided order ID

        Args:
            order_ID (integer): ID number of order to be obtained

        Returns:
            Order: Item of type Order based off provided ID
        """
        return next((i for i in self.orders if i.id == order_id), None)
    
    def get_order_from_history(self, order_id) -> Order:
        """Returns a specific order based off provided order ID from the history

        Args:
            order_id (int): ID number of order to be obtained

        Returns:
            Order: Item of type Order based off provided ID
        """
        return next((i for i in self.history if i.id == order_id), None)
    
    def get_table_from_order(self, order_ID) -> Table:
        """ Given an order ID, finds the table that the order belongs to

        Args:
            order_ID (Integer): ID number of order to use to find the table

        Returns:
            Table: Table object that has the order specified by the order ID
        """
        for i in self.map.keys():
            if order_ID in self.map[i]:
                return i
    
    def get_table_orders(self, table_id: int) -> list[Order]:
        """ Returns a list of orders at a specific table

        Args:
            table_id (integer): ID of table to acquire the orders of

        Raises:
            ValueError: Raised when table does not exist

        Returns:
            list[Order]: List of orders of the table specified by the table ID
        """
        if table_id not in self.map.keys():
            raise ValueError("OrderManager: get_table_orders(): table_id does not exist in map")
        
        order_ids = self.map[table_id]
        order_list = []
        for i in self.orders:
            if i.id in order_ids:
                order_list.append(i)

        return order_list
    
    def add_order(self, order: Order, table: Table):
        """ Adding orders to list of orders and relational map

        Args:
            order (Order): Order object to be added to the table
            table (Table): Table object to acquire an order

        Raises:
            ValueError: Raised when table already has that order object
        """
        if order in self.__orders:
            raise ValueError("OrderManager: add_order(): Order already exists")
        self.orders.append(order)
        self.history.append(order)

        if table.id in self.__map.keys():
            self.__map[table.id] += [order.id]
        else:
            self.__map[table.id] = [order.id]
        table.add_order(order)

    def remove_order(self, order: Order, table: Table):
        """ Removing orders from list of orders and relational map

        Args:
            order (Order): Order object to be removed from the table
            table (Table): Table object to lose an order

        Raises:
            ValueError: Raised when table does not have that order object
        """
        if order not in self.__orders:
            raise ValueError("OrderManager: remove_order(): Order does not exist")

        if table.id in self.map.keys():
            self.__map[table.id].remove(order.id)
            table.remove_order(order)
            self.orders.remove(order)
        else:
            raise ValueError("OrderManager: remove_order(): Table does not have supplied order")
        
    def change_state(self, order: int | Order):
        """ Move item along to the next stage

        Args:
            order (integer | Order): Object to have its state progressed to the 
            next state

        Raises:
            TypeError: Raised when order argument is not of type Order or Integer
        """
        if isinstance(order, int):
            order = self.get_order(order)
        elif isinstance(order, Order):
            pass
        else:
            raise TypeError("OrderManager: change_state(): Not a valid Order obj or order_id")
        order.change_state()

    def change_menu_item_state(self, order: int | Order, id: int):
        """ Changes the menu_item state of a menu_item within a specified order

        Args:
            order (int | Order): the order housing the menu_item to be changed
            id (int): the order-specific id of the menu_item to be changed

        Raises:
            TypeError: The order passed in (or order_id) is invalid
        """
        if isinstance(order, int):
            order = self.get_order(order)
        elif isinstance(order, Order):
            pass
        else:
            raise TypeError("OrderManager: change_state(): Not a valid Order obj or order_id")
        
        order.change_menu_item_state_by_id(id)


    def change_to_state(self, order: int | Order, string: str) -> bool:
        """ Move item along to a specified state

        Args:
            order (integer | Order): Object to have its state changed
            string (str): The new state of the order object

        Raises:
            TypeError: Raised when order argument is not of type Order or Integer

        Returns:
            Boolean: True or false whether the change was successful or not. 
            True if change was successful and false if the string was invalid
        """
        if isinstance(order, int):
            order = self.get_order(order)
        elif isinstance(order, Order):
            pass
        else:
            raise TypeError("OrderManager: change_to_state(): Not a valid Order obj or order_id")
        
        if string in States.list():
            while order.state != string:
                order.change_state()
            return True
        
        return False

    def calculate_table_bill(self, table_id: int) -> Bill:
        """ Calculates the current table bill from the table's list of orders

        Args:
            table_id (integer): ID of the table

        Raises:
            TypeError: Raised when there is an invalid table ID
            ValueError: Raised when the table has no orders

        Returns:
            Bill: Current bill object for the specified table
        """
        if isinstance(table_id, int):
            pass
        else:
            raise TypeError("OrderManager: calculate_table_bill(): Not a valid id")
        
        bills = [i.calculate_bill() for i in self.get_table_orders(table_id)]
        
        if None in bills:
            raise ValueError("OrderManager: calculate_table_bill(): One or more orders have not been served yet")
        
        subtotal = sum([i.price for i in bills if i.paid == False])
        
        return Bill(subtotal)
    
    def orders_json(self) -> dict:
        """ Creates a dictionary with a list containing all of the current orders
        without table ids
        
        Returns:
            dict: Dictionary containing a list of all the current orders
        """
        return {
            "orders": [i.jsonify() for i in self.orders]
            }
    
    def history_json(self) -> dict:
        """ Creates a dictionary with a list containing all of the current and
        previous orders

        Returns:
            dict: Dictionary containing a list of all current and previous
            orders
        """
        return {
            "history": [i.jsonify(self.get_table_from_order(i.id)) for i in self.history]
        }
    
    def jsonify(self) -> dict:
        """ Creates a dictionary with a list containing all of the orders of 
        each individual table

        Returns:
            dict: Dictionary containing a list of all of the orders of 
        each individual table
        """
        return {
            "orders": [i.jsonify(self.get_table_from_order(i.id)) for i in self.orders]
            }



