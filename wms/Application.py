from __future__ import annotations
from wms import UserHandler, TableHandler, MenuHandler, Menu, SRMHandler, ServiceRequestManager, OrderManagerHandler, OrderManager, RestaurantManagerHandler, RestaurantManager, PersonalisedDealEngine
from wms.DbHandler import *
from sqlalchemy.orm import Session
from sqlalchemy import select


class Application():
    def __init__(self):
        """ Constructor for the Application class. A decorator class for
        managing the app
        """
        self.__db_handler = DbHandler()
        self.__user_handler = UserHandler(self.db_handler)
        self.__table_handler = TableHandler()
        self.__menu_handler = MenuHandler(Menu(self.db_handler), self.db_handler)
        self.__srm_handler = SRMHandler(
            ServiceRequestManager(self.db_handler),
            self.user_handler,
        )
        self.__om_handler = OrderManagerHandler(
            OrderManager(),
            self.table_handler,
            self.menu_handler,
            self.db_handler
        )
        self.__restaurant_manager_handler = RestaurantManagerHandler(
            RestaurantManager(),
            self.menu_handler,
            self.om_handler,
            self.table_handler,
            self.user_handler
        )
        self.__pd_engine = PersonalisedDealEngine(
            self.user_handler,
            self.om_handler
        )

        # self.db_handler.initialise()
        self.initialise_db()

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

    @property
    def db_handler(self) -> DbHandler:
        """ Returns the DbHandler object."""
        return self.__db_handler

    def initialise_db(self):
        with Session(self.db_handler.engine) as session:
            res = session.scalars(select(Category).order_by(Category.id)).fetchall()
            for c in res:
                print(f'\n\nCategories in database: {c}\n\n')
                self.menu_handler.add_category(str(c.name))
            print(f'\n\nCategories converted to objects: {self.menu_handler.menu.categories}\n\n')


            res = session.execute(select(MenuItem, Category).join(MenuItem.category).order_by(MenuItem.id, Category.id))
            # print(res)
            for c in res:
                self.menu_handler.add_menu_item(c.Category.name, c.MenuItem.name, c.MenuItem.price, c.MenuItem.image_url)
            for m in self.menu_handler.menu.menu_items():
                print(f'\n\nMenu Items converted to objects: {m.name}\n\n')
