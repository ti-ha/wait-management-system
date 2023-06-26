from .User import User
from .Order import Order, State
from .OrderManager import OrderManager

class WaitStaff(User):
    def __init__(self, firstname, lastname, order_manager):
        super().__init__(firstname, lastname)
        self.__requests = []
        self.__order_manager = order_manager
        self.__order_manager.observer_attach(self)

    # Get list of requests
    def get_requests(self):
        return self.__requests
    
    def assign_requests(self, order):
        if not isinstance(order, Order):
            raise TypeError("WaitStaff: assign_requests(): Object is not of type Order")
        
        if order not in self.__requests:
            self.__requests.append(order)
            # print("Added order number " + str(order.get_id()) + " to Wait Staff")

    def remove_requests(self, order):
        if not isinstance(order, Order):
            raise TypeError("WaitStaff: remove_requests(): Object is not of type Order")
        
        if order in self.__requests:
            self.__requests.remove(order)
            # print("Removed order number " + str(order.get_id()) + " from Wait Staff") 

    def order_manager_update(self, orders):
        for order in orders:
            if order.get_state() == State.COOKED:
                self.assign_requests(order)
            else:
                self.remove_requests(order)