from __future__ import annotations
from wms import *

class Application():
    def __init__(self):
        """ Constructor for the Application class. A decorator class for 
        managing the app
        """
        self.__menu_handler = MenuHandler(Menu())
        self.__table_handler = TableHandler()
        self.__om_handler = OrderManagerHandler(OrderManager(), self.table_handler, self.menu_handler)
        self.__user_handler = UserHandler()
        self.__srm_handler = SRMHandler(ServiceRequestManager())
        self.__restaurant_manager_handler = RestaurantManagerHandler(RestaurantManager(), self.menu_handler)

    @property
    def menu_handler(self) -> MenuHandler:
        return self.__menu_handler
    
    @property
    def table_handler(self) -> TableHandler:
        return self.__table_handler
    
    @property
    def om_handler(self) -> OrderManagerHandler:
        return self.__om_handler
    
    @property
    def user_handler(self) -> UserHandler:
        return self.__user_handler
    
    @property
    def srm_handler(self) -> SRMHandler:
        return self.__srm_handler
    
    @property
    def restaurant_manager_handler(self) -> RestaurantManagerHandler:
        return self.__restaurant_manager_handler