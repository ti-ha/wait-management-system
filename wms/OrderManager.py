from __future__ import annotations
from .Order import Order, States
from .User import User
from .Table import Table
from .Bill import Bill

class OrderManager:
    def __init__(self):
        """# Constructor for the Order Manager class
        """
        self.__orders = []

        # maps table: [orders]
        self.__map = {}
        
    # Getter
    def get_orders(self) -> list[Order]:
        return self.__orders
    
    def get_map(self) -> dict:
        return self.__map
    
    def get_order(self, order_ID) -> Order:
        """ Returns a specific order based off provided order ID

        Args:
            order_ID (integer): ID number of order to be obtained

        Returns:
            Order: Item of type Order based off provided ID
        """
        for order in self.get_orders():
            if (order.id == order_ID):
                return order
        return None
    
    def get_table_from_order(self, order_ID) -> int:
        """ TODO

        Args:
            order_ID (_type_): _description_

        Returns:
            int: _description_
        """
        for i in self.get_map().keys():
            if order_ID in self.get_map()[i]:
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
        if table_id not in self.get_map().keys():
            raise ValueError("OrderManager: get_table_orders(): table_id does not exist in map")
        
        order_ids = self.get_map()[table_id]
        order_list = []
        for i in self.get_orders():
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
        self.__orders.append(order)
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

        if table.id in self.get_map().keys():
            self.__map[table.id].remove(order.id)
            table.remove_order(order)
            self.__orders.remove(order)
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
        if string.upper() in States.list():
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
        
        orderlist = self.get_table_orders(table_id)
        bills = []
        for i in orderlist:
            bills.append(i.bill)
        
        if None in bills:
            raise ValueError("OrderManager: calculate_table_bill(): One or more orders have not been served yet")
        
        subtotal = 0
        for i in bills:
            if i.is_paid() == False:
                subtotal += i.get_price()
        
        return Bill(subtotal)
    
    def orders_json(self) -> dict:
        """ Creates a dictionary with a list containing all of the current orders

        Returns:
            dict: Dictionary containing a list of all the current orders
        """
        output = {"orders": []}
        for i in self.get_orders():
            output["orders"].append(i.jsonify())
        
        return output
    
    def jsonify(self) -> dict:
        """ TODO:

        Returns:
            dict: _description_
        """
        output = {"orders": []}
        for i in self.get_orders():
            table_id = self.get_table_from_order(i.id)
            output["orders"].append(i.jsonify(table_id))
        
        return output



