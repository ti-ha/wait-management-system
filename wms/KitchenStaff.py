from User import User
from Order import Order

class KitchenStaff(User):
    def __init__(self, firstname, lastname):
        super().__init__(firstname, lastname)
        self.__orders = []

    # Add to list of orders
    def assign_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("Kitchen Staff: assign_order(): Object is not of type Order")
        self.__orders.append(order)

    # Remove order once complete
    def remove_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("Kitchen Staff: remove_order(): Object is not of type Order")
        self.__orders.remove(order)