from .Order import Order
from .User import User

class OrderManager:
    # Constructor for the Order Manager class
    def __init__(self):
        self.__orders = []
        
    # Getter
    def orders(self) -> list[Order]:
        return self.__orders
    
    # Adding orders to list of orders
    def add_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("OrderManager: add_order(): Object is not of type Order")
        
        if order in self.__orders:
            raise ValueError("OrderManager: add_order(): Order already exists")
        self.__orders.append(order)

    # Returns a specific order based off provided order ID
    def get_order(self, order_ID) -> Order:
        for order in self.orders():
            if (order.id() == order_ID):
                return order
        return ValueError("OrderManager: get_order(): Order doesn't exist")
        
    # Move item along to the next stage
    def change_state(self, order_ID):
        order = self.get_order(order_ID)
        if not isinstance(order, Order):
            raise TypeError("OrderManager: mark_as_complete(): Object is not of type Order")
        order.change_state()


