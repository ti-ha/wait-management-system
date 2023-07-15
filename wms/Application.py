from wms import *
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


class Application():
    def __init__(self):

        """ Constructor for the Application class. A decorator class for 
        managing the app
        """
        # database engine
        db_engine = create_engine("sqlite+pysqlite:///wms_db.db", echo=True)

        self.menu_handler = MenuHandler(Menu(), db_engine)
        self.table_handler = TableHandler()
        self.om_handler = OrderManagerHandler(OrderManager(), self.table_handler, self.menu_handler)
        self.user_handler = UserHandler()
        self.srm_handler = SRMHandler(ServiceRequestManager())
        self.restaurant_manager_handler = RestaurantManagerHandler(RestaurantManager(), self.menu_handler)

       

           