from __future__ import annotations
from wms import *

class Application():
    def __init__(self):
        """ Constructor for the Application class. A decorator class for 
        managing the app
        """
        self.__user_handler = UserHandler()
        self.__table_handler = TableHandler()
        self.__menu_handler = MenuHandler(Menu())
        self.__srm_handler = SRMHandler(ServiceRequestManager(), self.user_handler)
        self.__restaurant_manager_handler = RestaurantManagerHandler(RestaurantManager(), self.menu_handler, self.table_handler, self.user_handler)
        self.__om_handler = OrderManagerHandler(OrderManager(), self.table_handler, self.menu_handler)
        self.__pd_engine = PersonalisedDealEngine(self.user_handler, self.om_handler)

    @property
    def menu_handler(self) -> MenuHandler:
        """ Returns the MenuHandler object."""
        return self.__menu_handler
    
    @property
    def table_handler(self) -> TableHandler:
        """ Returns the TableHandler object."""
        return self.__table_handler
    
    @property
    def om_handler(self) -> OrderManagerHandler:
        """ Returns the OrderManagerHandler object."""
        return self.__om_handler
    
    @property
    def user_handler(self) -> UserHandler:
        """ Returns the UserHandler object."""
        return self.__user_handler
    
    @property
    def srm_handler(self) -> SRMHandler:
        """ Returns the ServiceRequestManager Handler object."""
        return self.__srm_handler
    
    @property
    def restaurant_manager_handler(self) -> RestaurantManagerHandler:
        """ Returns the RestaurantManagerHandler object."""
        return self.__restaurant_manager_handler
    
    @property
    def pd_engine(self) -> PersonalisedDealEngine:
        """ Returns the Personalised Deal Engine """
        return self.__pd_engine