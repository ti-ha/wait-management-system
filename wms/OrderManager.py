from .Order import Order
from .User import User
from .Table import Table

class OrderManager:
    # Constructor for the Order Manager class
    def __init__(self):
        self.__orders = []

        # maps table: [orders]
        self.__map = {}
        
    # Getter
    def orders(self) -> list[Order]:
        return self.__orders
    
    def map(self) -> dict:
        return self.__map
    
    # Returns a specific order based off provided order ID
    def get_order(self, order_ID) -> Order:
        for order in self.orders():
            if (order.id() == order_ID):
                return order
        raise ValueError("OrderManager: get_order(): Order doesn't exist")
    
    # Returns a list of orders at a specific table
    def get_table_orders(self, table_id: int) -> list[Order]:
        if table_id not in self.map().keys():
            raise ValueError("OrderManager: get_table_orders(): table_id does not exist in map")
        
        order_ids = self.map()[table_id]
        order_list = []
        for i in self.orders():
            if i.id() in order_ids:
                order_list.append(i)

        return order_list
    
    # Adding orders to list of orders and relational map
    def add_order(self, order: Order, table: Table):
        if order in self.__orders:
            raise ValueError("OrderManager: add_order(): Order already exists")
        self.__orders.append(order)
        self.__map[table.get_id()] += [order.id()]
        table.add_order(order)

    # Removing orders from list of orders and relational map
    def remove_order(self, order: Order, table: Table):
        if order not in self.__orders:
            raise ValueError("OrderManager: remove_order(): Order does not exist")

        if table.get_id() in self.map().keys():
            self.__map[table.get_id()].remove(order.id())
            table.remove_order(order)
            self.__orders.remove(order)
        else:
            raise ValueError("OrderManager: remove_order(): Table does not have supplied order")
        
    # Move item along to the next stage
    def change_state(self, order_ID):
        order = self.get_order(order_ID)
        if not isinstance(order, Order):
            raise TypeError("OrderManager: mark_as_complete(): Object is not of type Order")
        order.change_state()


