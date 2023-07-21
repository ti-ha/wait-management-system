from __future__ import annotations
from wms import User, ServiceRequest

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
    def requests(self) -> list[ServiceRequest]:
        """ Returns the wait staff's list of requests """
        return self.__requests
    
    def assign_requests(self, order):
        """ Add a request to the list of requests

        Args:
            order (Order): Order to be added to the list of requests

        Raises:
            TypeError: Raised when order argument is not of type Order
            ValueError: Raised when the Order already exists
        """
        if not isinstance(order, ServiceRequest):
            raise TypeError("WaitStaff: assign_requests(): Object is not of type ServiceRequest")
        
        if order in self.__requests:
            raise ValueError("WaitStaff: assign_requests(): Request already exists")
        
        self.__requests.append(order)

    def remove_requests(self, request):
        """ Remove an order from the list of requests

        Args:
            order (Order): Order to be removed from the list of requests

        Raises:
            TypeError: Raised when order argument is not of type Order
            ValueError: Raised when the Order does not exist
        """
        if not isinstance(request, ServiceRequest):
            raise TypeError("WaitStaff: remove_requests(): Object is not of type ServiceRequest")
        
        if request not in self.__requests:
            raise ValueError("WaitStaff: remove_requests(): Request does not exist")
        # Move order to complete
        self.requests.remove(request) 