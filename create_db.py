from wms import Application

MEATLOAF_URL =  "https://www.spendwithpennies.com/wp-content/uploads/2022/12/1200-The-Best-Meatloaf-Recipe-SpendWithPennies.jpg"
ARANCINI_BALLS_URL = "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/arancini_balls-db2b1df.jpg?quality=90&webp=true&resize=440,400"
GREEK_SALAD_URL = "https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2018/08/Greek-Salad-main.jpg"
SALT_AND_PEPPER_SQUID_URL = "https://redhousespice.com/wp-content/uploads/2022/02/squid-with-salt-and-pepper-seasoning-scaled.jpg"
PLACEHOLDER = "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg"

def create_tables(app):
    """Build database from scratch

    Args:
        app (Application): app for the database to be build
    """
    menu = app.menu_handler
    
    menu.add_category("Entrees")
    menu.add_menu_item("Entrees", "Meatloaf", 3, MEATLOAF_URL)
    menu.add_menu_item("Entrees", "Arancini Balls", 9, ARANCINI_BALLS_URL)
    menu.add_menu_item("Entrees", "Greek Salad", 6.5, GREEK_SALAD_URL)
    menu.add_menu_item("Entrees", "Salt and Pepper Squid", 8.5, SALT_AND_PEPPER_SQUID_URL)

    menu.add_category("Mains")
    menu.add_menu_item("Mains", "Burger", 12, PLACEHOLDER)
    menu.add_menu_item("Mains", "Item 2", 12, PLACEHOLDER)
    menu.add_menu_item("Mains", "Item 3", 12, PLACEHOLDER)
    menu.add_menu_item("Mains", "Item 4", 12, PLACEHOLDER)
    menu.add_menu_item("Mains", "Item 5", 12, PLACEHOLDER)
    menu.add_menu_item("Mains", "Item 6", 12, PLACEHOLDER)

    menu.add_category("Snacks")
    menu.add_menu_item("Snacks", "Item 7", 10, PLACEHOLDER)
    menu.add_menu_item("Snacks", "Item 8", 10, PLACEHOLDER)
    menu.add_menu_item("Snacks", "Item 9", 10, PLACEHOLDER)
    menu.add_menu_item("Snacks", "Item 10", 10, PLACEHOLDER)
    menu.add_menu_item("Snacks", "Item 11", 10, PLACEHOLDER)

    menu.add_deal(5.0, ["Meatloaf", "Burger"])          # Deal 0
    menu.add_deal(5.0, ["Arancini Balls", "Burger"])    # Deal 1
    menu.add_deal(10.0, ["Greek Salad", "Burger"])      # Deal 2

    table = app.table_handler

    table.add_table(5, None)                # Table 0
    table.add_table(5, None)                # Table 1
    table.add_table(5, None)                # Table 2
    table.add_table(5, None)                # Table 3
    table.add_table(5, None)                # Table 4

    order = app.om_handler
    
    order.add_order(0, [0, 1], [], None)
    order.change_order_state(0)
    order.change_order_state(0)

    order.add_order(1, [], [1], None)
    order.change_order_state(1)
    order.change_order_state(1)
    order.change_order_state(1)

    order.add_order(2, [5, 6], [0, 1, 2], None)
    order.change_order_state(2)
    order.change_order_state(2)
    order.change_order_state(2)

    user = app.user_handler

    user.add_user("Manager", "A", "Manager", "12345")
    user.add_user("Customer", "A", "Customer", "12345")
    user.add_user("WaitStaff", "A", "WaitStaff", "12345")
    user.add_user("KitchenStaff", "A", "KitchenStaff", "12345")

    user.login("Manager", "A", "12345")
    user.logout("Manager", "A")
    user.login("Manager", "A", "12345")

    srm = app.srm_handler.srm

    srm.add_request(0, "Spoon", "I need an extra spoon")

def main():
    app = Application()
    app.om_handler.add_order(0, [1], [], None)
    app.om_handler.add_order(0, [1, 2], [], None)
    app.om_handler.add_order(0, [1, 2, 3], [], None)

    # create_tables(app)

if __name__ == '__main__':
    main()