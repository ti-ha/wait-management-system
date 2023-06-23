from .Order import Order
from .User import User

class OrderManager:
    # Constructor for the Order Manager class
    def __init__(self):
        self.__orders = []
        
    # Getter
    def get_orders(self):
        return self.__orders
    
    # Adding orders to list of orders
    def add_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("OrderManager: add_order(): Object is not of type Order")
        
        if order in self.__orders:
            raise ValueError("OrderManager: add_order(): Order already exists")
        self.__orders.append(order)

    # Returns a specific order based off provided integer
    def get_order(self, orderNum):
        if orderNum > len(self.__orders):
            return ValueError("OrderManager: get_order(): Not enough orders")
        return self.__orders[orderNum]
    
    # Move item along to the next stage
    def mark_as_complete(self, order):
        if not isinstance(order, Order):
            raise TypeError("OrderManager: mark_as_complete(): Object is not of type Order")
        
        if order not in self.__orders:
            raise ValueError("OrderManager: mark_as_complete(): Order does not exists")

        orderIndex = self.__orders.index(order)
        self.__orders(orderIndex).change_state()
