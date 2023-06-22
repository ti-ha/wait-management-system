from User import User
from Order import Order

class WaitStaff(User):
    def __init__(self, firstname, lastname):
        super().__init__(firstname, lastname)
        self.__requests = []

    # Get list of requests
    def get_requests(self):
        return self.__requests
    
    def assign_requests(self, order):
        if not isinstance(order, Order):
            raise TypeError("WaitStaff: assign_requests(): Object is not of type Order")
        
        if order in self.__requests:
            raise ValueError("WaitStaff: assign_requests(): Order already exists")
        self.__requests.append(order)

    def remove_requests(self, order):
        if not isinstance(order, Order):
            raise TypeError("WaitStaff: remove_requests(): Object is not of type Order")
        
        if order not in self.__requests:
            raise ValueError("WaitStaff: remove_requests(): Order does not exist")
        orderNum = self.__requests.index(order)
        self.__requests[orderNum].change_state()
        # Move order to complete
        self.__requests.remove(order) 