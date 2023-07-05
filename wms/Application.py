from wms import *
import json

# A decorator class for managing the app
class Application():
    def __init__(self):
        self.menu_handler = MenuHandler(Menu())
        self.table_handler = TableHandler()
        self.om_handler = OrderManagerHandler(OrderManager(), self.table_handler, self.menu_handler)
        self.user_handler = UserHandler()
        self.__service_request_manager = ServiceRequestManager()
        self.__restaurant_manager = RestaurantManager(self.menu_handler)