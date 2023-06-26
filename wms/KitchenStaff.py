from .User import User
from .Order import Order
from .OrderManager import OrderManager

class KitchenStaff(User):
    def __init__(self, firstname, lastname, order_manager):
        super().__init__(firstname, lastname)
        self.__orders = []
        self.__order_manager = order_manager
        self.__order_manager.observer_attach(self)

    def get_orders(self):
        return self.__orders
    
    # Add to list of orders
    def assign_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("KitchenStaff: assign_order(): Object is not of type Order")
        
        if order not in self.__orders:
            self.__orders.append(order)

    # Remove order once complete
    def remove_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("KitchenStaff: remove_order(): Object is not of type Order")
        
        if order in self.__orders:
            self.__orders.remove(order) 

    # Order manager observer update
    def order_manager_update(self, orders):
        for order in orders:
            if order.state() == "ordered":
                self.assign_order(order)
            elif order.state() == "cooking":
                self.__order_manager.change_state(order)
            else:
                self.remove_order(order)