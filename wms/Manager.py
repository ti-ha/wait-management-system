from .User import User
from .OrderManager import OrderManager

# Has no other attributes differentiating itself from a user
# only important difference is type. Also can see OrderManager
class Manager(User):
    def __init__(self, firstname, lastname, order_manager):
        super().__init__(firstname, lastname)
        self.__order_manager = order_manager
        self.__order_manager.observer_attach(self)
        pass

    def order_manager_update(self, orders):
        return