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
        self.__table_handler = TableHandler(self.db_handler)
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
        """Create objects from database"""
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
                self.menu_handler.add_menu_item(it.Category.name, it.MenuItem.name,
                                                it.MenuItem.price, it.MenuItem.image_url)
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

            ### TABLES
            tables = session.scalars(select(Table.limit).order_by(Table.id)).fetchall()
            print(tables)
            for table in tables:
                self.table_handler.add_table(table, None)

            print(json.dumps(self.table_handler.jsonify(), indent=4))

            ### ORDERS
            orders = session.execute(select(Order.id, Order.table_id, 
                                            Order.state)).fetchall()
            order_deal = session.execute(select(Order.id, Deal.id)
                                         .join(Order.deals)).fetchall()
            order_menu = session.execute(select(Order.id, MenuItem.id)
                                         .join(Order.menu_items)).fetchall()
            
            for order, table, state in orders:
                deals = []
                for o1, deal in order_deal:
                    if o1 == order:
                        deals.append(deal)
                items = []
                for o2, item in order_menu:
                    if o2 == order:
                        items.append(item)
                self.om_handler.add_order(table, items, deals)

                ## TODO set states
                # self.om_handler.order_manager.set_state(order, state)
                print(json.dumps(self.om_handler.jsonify_orders(), indent=4))
            # states = session.execute(select(Order.id, Order.s))

            ### USERS
            users = session.execute(select(User.first_name, User.last_name, 
                                           User.type, User.password_hash)).fetchall()
            
            ## TODO add user using hashed password
            for fn, ln, type, phash in users:
                print(f'\n\n{fn} {ln} {type} {phash} \n\n')
            # self.user_handler.add_user()
            print(json.dumps(self.user_handler.jsonify(), indent=4))
      



