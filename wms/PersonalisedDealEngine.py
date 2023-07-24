from wms import OrderManagerHandler, UserHandler,  MenuHandler

class PersonalisedDealEngine():
    def __init__(self, user_handler, order_manager_handler):
        self.__user_handler = user_handler
        self.__order_manager_handler = order_manager_handler

    @property
    def user_handler(self) -> UserHandler:
        return self.__user_handler
    
    @property
    def order_manager_handler(self) -> OrderManagerHandler:
        return self.__order_manager_handler
    
    @property
    def menu_handler(self) -> MenuHandler:
        return self.order_manager_handler.menu_handler