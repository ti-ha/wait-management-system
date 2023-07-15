from wms import *
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


class Application():
    def __init__(self):
        """ Constructor for the Application class. A decorator class for 
        managing the app
        """
        self.menu_handler = MenuHandler(Menu())
        self.table_handler = TableHandler()
        self.om_handler = OrderManagerHandler(OrderManager(), self.table_handler, self.menu_handler)
        self.user_handler = UserHandler()
        self.srm_handler = SRMHandler(ServiceRequestManager())
        self.restaurant_manager_handler = RestaurantManagerHandler(RestaurantManager(), self.menu_handler)

        # database engine
        self.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

        stmt = text("CREATE TABLE some_table(x int)") 
        stmt1 = text("INSERT INTO some_table (x) VALUES (3)")
        stmt2 = text("SELECT * from some_table")
        with Session(self.engine) as session:
            session.execute(stmt)
            session.execute(stmt1)
            session.commit()
            result = session.execute(stmt2)
            for row in result:
                print(f"HELLO {row}")