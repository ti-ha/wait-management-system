from wms import *

MEATLOAF_URL =  "https://www.spendwithpennies.com/wp-content/uploads/2022/12/1200-The-Best-Meatloaf-Recipe-SpendWithPennies.jpg"
ARANCINI_BALLS_URL = "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/arancini_balls-db2b1df.jpg?quality=90&webp=true&resize=440,400"
GREEK_SALAD_URL = "https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2018/08/Greek-Salad-main.jpg"
SALT_AND_PEPPER_SQUID_URL = "https://redhousespice.com/wp-content/uploads/2022/02/squid-with-salt-and-pepper-seasoning-scaled.jpg"
PLACEHOLDER = "https://t4.ftcdn.net/jpg/01/69/56/95/360_F_169569546_zaLG8x4tyIu3SDn1jYWXThVpMjCEbn8Q.jpg"

if __name__ == '__main__':
    app = Application()
    menu = app.menu_handler

    menu.add_category("Entrees")
    menu.get_category("Entrees").add_menu_item(MenuItem("Meatloaf", 3, MEATLOAF_URL), menu.db)
    menu.get_category("Entrees").add_menu_item(MenuItem("Arancini Balls", 9, ARANCINI_BALLS_URL), menu.db)
    menu.get_category("Entrees").add_menu_item(MenuItem("Greek Salad", 6.5, GREEK_SALAD_URL), menu.db)
    menu.get_category("Entrees").add_menu_item(MenuItem("Salt and Pepper Squid", 8.5, SALT_AND_PEPPER_SQUID_URL), menu.db)

    menu.add_category("Mains")
    menu.get_category("Mains").add_menu_item(MenuItem("Burger", 12, PLACEHOLDER), menu.db)
    menu.get_category("Mains").add_menu_item(MenuItem("Item 2", 12, PLACEHOLDER), menu.db)
    menu.get_category("Mains").add_menu_item(MenuItem("Item 3", 12, PLACEHOLDER), menu.db)
    menu.get_category("Mains").add_menu_item(MenuItem("Item 4", 12, PLACEHOLDER), menu.db)
    menu.get_category("Mains").add_menu_item(MenuItem("Item 5", 12, PLACEHOLDER), menu.db)
    menu.get_category("Mains").add_menu_item(MenuItem("Item 6", 12, PLACEHOLDER), menu.db)

    menu.add_category("Snacks")
    menu.get_category("Snacks").add_menu_item(MenuItem("Item 7", 10, PLACEHOLDER), menu.db)
    menu.get_category("Snacks").add_menu_item(MenuItem("Item 8", 10, PLACEHOLDER), menu.db)
    menu.get_category("Snacks").add_menu_item(MenuItem("Item 9", 10, PLACEHOLDER), menu.db)
    menu.get_category("Snacks").add_menu_item(MenuItem("Item 10", 10, PLACEHOLDER), menu.db)
    menu.get_category("Snacks").add_menu_item(MenuItem("Item 11", 10, PLACEHOLDER), menu.db)

