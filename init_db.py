import json
from sqlalchemy.orm import Session
from sqlalchemy import select
from wms import MenuHandler, TableHandler, OrderManagerHandler, UserHandler, DbHandler
from wms.DbHandler import Category, MenuItem, Deal, User, Table, Order


def init_categories(session: Session, menu_handler: MenuHandler):
    """Initialise categories from existing database

    Args:
        session (Session): SQLAlchemy session
        menu_handler (MenuHandler): Menu handler
    """
    categories = session.scalars(select(Category)).fetchall()
    for cat in categories:
        menu_handler.add_category(cat.name)
    # print(json.dumps(menu_handler.jsonify_categories(), indent=4))

def init_menu_items(session: Session, menu_handler: MenuHandler):
    """Initialise menu items from existing database

    Args:
        session (Session): SQLAlchemy session
        menu_handler (MenuHandler): Menu handler
    """
    items = session.execute(select(MenuItem, Category)
                            .join(MenuItem.category))
    for item in items:
        menu_handler.add_menu_item(item.Category.name, item.MenuItem.name,
                                   item.MenuItem.price, item.MenuItem.image_url)
    # print(json.dumps(menu_handler.jsonify(), indent=4))

def init_deals(session: Session, menu_handler: MenuHandler):
    """Initialise deals from existing database

    Args:
        session (Session): SQLAlchemy session
        menu_handler (MenuHandler): Menu handler
    """
    association = session.execute(select(Deal.id, Deal.discount, MenuItem.name)
                                 .join(MenuItem.deals)).fetchall()
    deals = session.scalars(select(Deal.id)).fetchall()
    for deal in deals:
        items = []
        disc = float(0)
        for d_id, d_discount, item_name in association:
            if d_id == deal:
                items.append(item_name)
                disc = d_discount
        menu_handler.add_deal(disc, items)
    # print(json.dumps(menu_handler.jsonify_deals(), indent=4))

def init_tables(session: Session, table_handler: TableHandler):
    """Initialise tables from existing database

    Args:
        session (Session): SQLAlchemy session
        table_handler (TableHandler): Table handler
    """
    tables = session.scalars(select(Table.limit).order_by(Table.id)).fetchall()
    print(tables)
    for table in tables:
        table_handler.add_table(table, None)

    # print(json.dumps(table_handler.jsonify(), indent=4))

def init_orders(session: Session, om_handler: OrderManagerHandler):
    """Initialise order history from existing database

    Args:
        session (Session): SQLAlchemy session
        om_handler (OrderManagerHandler): Order manager handler
    """
    orders = session.execute(select(Order.id, Order.table_id,
                                    Order.state, Order.customer)).fetchall()
    order_deal = session.execute(select(Order.id, Deal.id)
                                .join(Order.deals)).fetchall()
    order_menu = session.execute(select(Order.id, MenuItem.id)
                                .join(Order.menu_items)).fetchall()

    for order, table, state, customer in orders:
        deals = []
        for o_deal, deal in order_deal:
            if o_deal == order:
                deals.append(deal)
        items = []
        for o_menu, item in order_menu:
            if o_menu == order:
                items.append(item)
        om_handler.add_order(table, items, deals, customer)

        om_handler.order_manager.set_state(order, int(state))
    print(json.dumps(om_handler.jsonify_orders(), indent=4))

def init_users(session: Session, user_handler: UserHandler):
    """Initialise users from existing database

    Args:
        session (Session): SQLAlchemy session
        user_handler (UserHandler): User handler
    """
    users = session.execute(select(User.first_name, User.last_name,
                                   User.type, User.password_hash)).fetchall()

    for first, last, utype, phash in users:
        user_handler.add_user(first, last, utype, "", phash)
    # print(json.dumps(user_handler.jsonify(), indent=4))

def initialise_db(db_handler: DbHandler, menu_handler: MenuHandler,
                  table_handler: TableHandler, om_handler: OrderManagerHandler,
                  user_handler: UserHandler):
    """Initialise server from existing database

    Args:
        db_handler (DbHandler): Database handler
        menu_handler (MenuHandler): Menu handler
        table_handler (TableHandler): Table handler
        om_handler (OrderManagerHandler): Order manager handler
        user_handler (UserHandler): User handler
    """
    with Session(db_handler.engine) as session:
        init_categories(session, menu_handler)
        init_menu_items(session, menu_handler)
        init_deals(session, menu_handler)
        init_tables(session, table_handler)
        init_orders(session, om_handler)
        init_users(session, user_handler)
