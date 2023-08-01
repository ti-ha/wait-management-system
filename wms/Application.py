from __future__ import annotations
from wms import UserHandler, TableHandler, MenuHandler, Menu, SRMHandler, ServiceRequestManager, OrderManagerHandler, OrderManager, RestaurantManagerHandler, RestaurantManager, PersonalisedDealEngine
from wms.DbHandler import *
from sqlalchemy.orm import Session
from sqlalchemy import select
import json

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

            ### CATEGORIES
            categories = session.scalars(select(Category)).fetchall()
            for cat in categories:
                self.menu_handler.add_category(cat.name)
            print(json.dumps(self.menu_handler.jsonify_categories(), indent=4))

            ### MENU ITEMS
            items = session.execute(select(MenuItem, Category)
                                    .join(MenuItem.category))
            for it in items:
                self.menu_handler.add_menu_item(
                    it.Category.name, 
                    it.MenuItem.name, 
                    it.MenuItem.price, 
                    it.MenuItem.image_url
                )
            print(json.dumps(self.menu_handler.jsonify(), indent=4))

            ### DEALS
            association = session.execute(select(Deal.id, Deal.discount, MenuItem.name)
                                          .join(MenuItem.deals)).fetchall()
            deals = session.scalars(select(Deal.id)).fetchall()
            for d in deals:
                items = []
                disc = float(0)
                for a in association:
                    if a[0] == d:
                        items.append(a[2])
                        disc = a[1]
                self.menu_handler.add_deal(disc, items)
            print(json.dumps(self.menu_handler.jsonify_deals(), indent=4))

            # ORDERS
            self.table_handler.add_table(10, None)
            self.table_handler.add_table(10, None)
            self.table_handler.add_table(10, None)
            self.table_handler.add_table(10, None)
            self.table_handler.add_table(10, None)

            orders = session.scalars(select(Order.id)).fetchall()
            order_deal = session.execute(select(Order.id, Deal.id).join(Order.deals)).fetchall()
            order_menu = session.execute(select(Order.id, MenuItem.id).join(Order.menu_items)).fetchall()
            
            print(orders)
            print(order_deal)
            print(order_menu)

            self.om_handler.order_manager.add_order(Order())

      



