from __future__ import annotations
from wms import User, Order

class WaitStaff(User):
    def __init__(self, firstname, lastname, password):
        """ Constructor of the WaitStaff class that inherits the User Class

        Args:
            firstname (string): First Name of the User
            lastname (string): Last Name of the User
            password (string): Password of the user
        """
        super().__init__(firstname, lastname, password)
        self.__requests = []

    @property
    def requests(self) -> list[Order]:
        """ Returns the wait staff's list of requests """
        return self.__requests
    
    def assign_requests(self, order):
        """ Add an order to the list of requests

        Args:
            order (Order): Order to be added to the list of requests

        Raises:
            TypeError: Raised when order argument is not of type Order
            ValueError: Raised when the Order already exists
        """
        if not isinstance(order, Order):
            raise TypeError("WaitStaff: assign_requests(): Object is not of type Order")
        
        if order in self.__requests:
            raise ValueError("WaitStaff: assign_requests(): Order already exists")
        self.__requests.append(order)

    def remove_requests(self, order):
        """ Remove an order from the list of requests

        Args:
            order (Order): Order to be removed from the list of requests

        Raises:
            TypeError: Raised when order argument is not of type Order
            ValueError: Raised when the Order does not exist
        """
        if not isinstance(order, Order):
            raise TypeError("WaitStaff: remove_requests(): Object is not of type Order")
        
        if order not in self.__requests:
            raise ValueError("WaitStaff: remove_requests(): Order does not exist")
        order_num = self.__requests.index(order)
        self.__requests[order_num].change_state()
        # Move order to complete
        self.__requests.remove(order) 