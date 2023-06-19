import User

class KitchenStaff(User):
    def __init__(self, firstname, lastname):
        super().__init__(self, firstname, lastname)
        self.__orders = []

    # Add to list of orders
    def assign_order(self, order):
        self.__orders.append(order)

    # Remove order once complete
    def remove_order(self, order):
        self.__orders.remove(order)