from wms import *

# A decorator class for managing the app
class Application():
    def __init__(self):
        self.menu_handler = MenuHandler(Menu())
        self.table_handler = TableHandler()
        self.om_handler = OrderManagerHandler(OrderManager(), self.table_handler, self.menu_handler)
        self.user_handler = UserHandler()
        self.srm_handler = SRMHandler(ServiceRequestManager())
        self.restaurant_manager_handler = RestaurantManagerHandler(RestaurantManager(), self.menu_handler)