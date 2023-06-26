from .Order import Order
from .User import User

class OrderManager:
    # Constructor for the Order Manager class
    def __init__(self):
        self.__orders = []
        self.__observers = []
        
    # Getter
    def get_orders(self):
        return self.__orders
    
    def observer_attach(self, observer):
        self.__observers.append(observer)

    def observer_update(self):
        for observer in self.__observers:
            observer.order_manager_update(self.__orders)

    # Adding orders to list of orders
    def add_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("OrderManager: add_order(): Object is not of type Order")
        
        if order in self.__orders:
            raise ValueError("OrderManager: add_order(): Order already exists")
        self.__orders.append(order)
        self.observer_update()

    # Returns a specific order based off provided order ID
    def get_order(self, order_ID):
        for order in self.__orders:
            if (order.get_id() == order_ID):
                return order
        return ValueError("OrderManager: get_order(): Order doesn't exist")
        
    # Move item along to the next stage
    def progress_order(self, order_ID):
        order = self.get_order(order_ID)
        if not isinstance(order, Order):
            raise TypeError("OrderManager: progress_order(): Object is not of type Order")
        order.change_state()
        self.observer_update()
