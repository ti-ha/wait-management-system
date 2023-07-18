# from wms import Menu, Category, MenuItem, Deal

# menu = Menu()
# burgers = Category("burgers")
# snacks = Category("snacks")
# burger = MenuItem("burger", 20.0, None)
# snack = MenuItem("snack",  20.0, None)
# drink = MenuItem("drink", 5.0, None)
# burgers.add_menu_item(burger)
# snacks.add_menu_item(snack)
# snacks.add_menu_item(drink)
# deal = Deal(0.50)
# deal.add_menu_item(snack)
# deal.add_menu_item(drink)
# menu.add_category(burgers)
# menu.add_category(snacks)
# menu.add_deal(deal)

# def test1(menu):
#     if len(menu.categories()) != 2:
#         print("test1 FAIL")
#         print(menu.categories())
#         return False

#     print("test1 PASS")
#     return True

# def test2(menu):
#     if len(menu.deals()) != 1:
#         print("test2 FAIL")
#         print(menu.deals())
#         return False

#     print("test2 PASS")
#     return True

# def test3(menu):
#     c = menu.get_category("burgers")
#     if c == None:
#         print("test3 FAIL")
#         return False

#     print("test3 PASS")
#     return True

# def test4(menu):
#     c = menu.get_category("burgers")
#     if c != burgers:
#         print("test4 FAIL")
#         print(c)
#         return False

#     print("test4 PASS")
#     return True

# def test5(menu):
#     c = Category("sides")
#     menu.add_category(c)
#     i = menu.get_category("sides")
#     if c != i:
#         print("test5 FAIL")
#         print(menu.categories())
#         return False

#     print("test5 PASS")
#     return True

# def test6(menu):
#     try:
#         menu.add_category(burgers)
#     except ValueError:
#         print("test6 PASS")
#         return True

#     print("test6 FAIL")
#     return False

# def test7(menu):
#     menu.remove_category("sides")
#     c = menu.get_category("sides")
#     if c != None:
#         print("test7 FAIL")
#         return False

#     print("test7 PASS")
#     return True

# def test8(menu):
#     try:
#         menu.add_deal(deal)
#     except ValueError:
#         print("test8 PASS")
#         return True

#     print("test8 FAIL")
#     return False

# def test9(menu):
#     newdeal = Deal(0.1)
#     menu.add_deal(newdeal)
#     if len(menu.deals()) != 2:
#         print("test9 FAIL")
#         return False

#     print("test9 PASS")
#     return True

# def test10(menu):
#     newdeal = menu.deals()[1]
#     menu.remove_deal(newdeal)
#     if len(menu.deals()) != 1:
#         print("test10 FAIL")
#         return False

#     print("test10 PASS")
#     return newdeal

# def test11(menu, out):
#     try:
#         menu.remove_deal(out)
#     except ValueError:
#         print("test11 PASS")
#         return True

#     print("test11 FAIL")
#     return False

# def test12(menu):
#     try:
#         menu.remove_category(24)
#     except TypeError:
#         print("test12 PASS")
#         return True

#     print("test12 FAIL")
#     return False

# def test13(menu):
#     try:
#         menu.remove_deal(69)
#     except TypeError:
#         print("test13 PASS")
#         return True

#     print("test13 FAIL")
#     return False

# def test14():
#     if burgers.id != 0 or snacks.id != 1:
#         print("test14 FAIL")
#         return False

#     newcat = Category("newcategory")
#     if newcat.id != 3:
#         print("test14 FAIL")
#         return False

#     print("test14 PASS")
#     return True

# def test15():
#     if burgers.name != "burgers":
#         print("test15 FAIL")
#         return False

#     print("test15 PASS")
#     return True

# def test16():
#     if len(burgers.menu_items) != 1 or len(snacks.menu_items) != 2:
#         print("test16 FAIL")
#         return False

#     print("test16 PASS")
#     return True

# # def test17():
# #     burger = MenuItem("burger", 20.0, None)
# #     o = burgers.is_menu_item(burger)
# #     if o.is_equal(burger):
# #         print("test17 FAIL")
# #         return False

# #     print("test17 PASS")
# #     return True

# def test18():
#     foo = MenuItem("foo", 33.0, None)
#     o = burgers.get_menu_item(foo)
#     if o != None:
#         print("test18 FAIL")
#         return False

#     print("test18 PASS")
#     return True

# def test19():
#     shoestring_fries = MenuItem("Shoestring fries", 33.0, None)
#     burgers.add_menu_item(shoestring_fries)
#     if burgers.get_menu_item(shoestring_fries) != None:
#         print("test19 PASS")
#         return shoestring_fries

#     print("test19 FAIL")
#     return False

# def test20(out):
#     shoestring_fries = MenuItem("Shoestring fries", 33.0, None)
#     burgers.remove_menu_item(out)
#     if burgers.get_menu_item(shoestring_fries) == None:
#         print("test20 PASS")
#         return True

#     print("test20 FAIL")
#     return False

# def test21():
#     try:
#         burgers.add_menu_item(burger)
#     except ValueError:
#         print("test21 PASS")
#         return True

#     print("test21 FAIL")
#     return False

# # def test22():
# #     try:
# #         burgers.add_menu_item(24)
# #     except TypeError:
# #         print("test22 PASS")
# #         return True

# #     print("test22 FAIL")
# #     return False

# # def test23(out):
# #     try:
# #         burgers.remove_menu_item(out)
# #     except ValueError:
# #         print("test23 PASS")
# #         return True

# #     print("test23 FAIL")
# #     return False

# # def test24():
# #     try:
# #         burgers.remove_menu_item(24)
# #     except TypeError:
# #         print("test24 PASS")
# #         return True

# #     print("test24 FAIL")
# #     return False

# # def test25():
# #     menu_item = MenuItem("test25", 25)
# #     if menu_item.name() != "test25":
# #         print("test25 FAIL")
# #         return False

# #     if menu_item.price() != 25:
# #         print("test25 FAIL")
# #         return False

# #     menu_item.set_name("test25_renamed")
# #     if menu_item.name() == "test25" or menu_item.name() != "test25_renamed":
# #         print("test25 FAIL")
# #         return False

# #     menu_item.set_price(26.69)
# #     if menu_item.price() == 25 or menu_item.price() != 26.69:
# #         print("test25 FAIL")
# #         return False

# #     print("test25 PASS")
# #     return True

# # def test26():
# #     menu_item = MenuItem("test26", 26)
# #     try:
# #         menu_item.set_name(26)
# #     except TypeError:
# #         pass
# #     else:
# #         print("test26 FAIL")
# #         return False

# #     try:
# #         menu_item.set_price("Burger")
# #     except TypeError:
# #         pass
# #     else:
# #         print("test26 FAIL")
# #         return False

# #     print("test26 PASS")
# #     return True

# # def test27():
# #     if MenuItem.isfloat("True"):
# #         print("test27 FAIL")
# #         return False
# #     print("test27 PASS")
# #     return True

# # def test28():
# #     if MenuItem.isfloat(42.0):
# #         print("test28 PASS")
# #         return True
# #     print("test28 FAIL")
# #     return False

# # def test29():
# #     deal = Deal(0.2)
# #     if deal.discount() != 0.2:
# #         print("test29 FAIL")
# #         return False

# #     if len(deal.menu_items()) != 0:
# #         print("test29 FAIL")
# #         return False

# #     menu_item = MenuItem("test29", 69)
# #     deal.add_menu_item(menu_item)
# #     if len(deal.menu_items()) != 1:
# #         print("test29 FAIL")
# #         return False

# #     try:
# #         deal.add_menu_item(menu_item)
# #     except ValueError:
# #         pass
# #     else:
# #         print("test29 FAIL")
# #         return False

# #     deal.remove_menu_item(menu_item)
# #     if len(deal.menu_items()) != 0:
# #         print("test29 FAIL")
# #         return False

# #     try:
# #         deal.remove_menu_item(menu_item)
# #     except ValueError:
# #         pass
# #     else:
# #         print("test29 FAIL")
# #         return False

# #     print("test29 PASS")
# #     return True

# # def test30():
# #     menu_item = MenuItem("test30", 30)
# #     deal = Deal(0.2, [menu_item])
# #     deal.set_discount(0.3)

# #     if deal.discount() != 0.3:
# #         print("test30 FAIL")
# #         return False

# #     try:
# #         deal.set_discount("Burger")
# #     except ValueError:
# #         pass
# #     else:
# #         print("test30 FAIL")
# #         return False

# #     if not deal.is_applicable(menu_item):
# #         print("test30 FAIL")
# #         return False

# #     deal.remove_menu_item(menu_item)
# #     if deal.is_applicable(menu_item):
# #         print("test30 FAIL")
# #         return False

# #     print("test30 PASS")
# #     return True

# # def test31():
# #     deal = Deal(6.9)
# #     try:
# #         deal.add_menu_item(Menu())
# #     except TypeError:
# #         pass
# #     else:
# #         print("test31 FAIL")
# #         return False
# #     try:
# #         deal.remove_menu_item(Menu())
# #     except TypeError:
# #         pass
# #     else:
# #         print("test31 FAIL")
# #         return False

# #     print("test31 PASS")
# #     return True

# # def test32():
# #     if Deal.isfloat(42.0):
# #         print("test32 PASS")
# #         return True
# #     print("test32 FAIL")
# #     return False


# if __name__ == '__main__':
#     #menu tests
#     test1(menu)
#     test2(menu)
#     test3(menu)
#     test4(menu)
#     test5(menu)
#     test6(menu)
#     test7(menu)
#     test8(menu)
#     test9(menu)
#     out = test10(menu)
#     test11(menu, out)
#     test12(menu)
#     test13(menu)
#     #category tests
#     test14()
#     test15()
#     test16()
#     # test17()
#     test18()
#     out1 = test19()
#     test20(out1)
#     test21()
#     # test22()
#     # test23(out1)
#     # test24()
#     # #menuitem tests
#     # test25()
#     # test26()
#     # test27()
#     # test28()
#     # #deal tests
#     # test29()
#     # test30()
#     # test31()
#     # test32()

import unittest
from wms import Application, Category, MenuItem, Deal, User, Customer, WaitStaff, KitchenStaff, Manager

class MenuTests(unittest.TestCase):
    """ Tests for menu handling functionality"""

    def setUp(self):
        self.app = Application()
        self.menu = self.app.menu_handler

    def test_add_category(self):
        """Add new category"""
        self.menu.add_category("Burgers")
        self.assertIsInstance(self.menu.get_category("Burgers"), Category)

    def test_add_category_twice(self):
        """Add new category twice"""
        self.menu.add_category("Burgers")
        with self.assertRaises(expected_exception=ValueError):
            self.menu.add_category("Burgers")

    def test_remove_category(self):
        """Remove existing category"""
        self.menu.add_category("Burgers")
        self.menu.remove_category("Burgers")
        self.assertIsNone(self.menu.get_category("Burgers"))

    def test_remove_category_nonexist(self):
        """Add menu item to non-existing category"""
        with self.assertRaises(expected_exception=ValueError):
            self.menu.remove_category("Burgers")

    def test_add_menu_item(self):
        """Add menu item to existing category"""
        self.menu.add_category("Burgers")
        self.menu.add_menu_item("Burgers", "Cheeseburger", 20.00, "/cheeseburger.png")
        self.assertIsInstance(self.menu.get_menu_item("Burgers", "Cheeseburger"), MenuItem)

    def test_add_menu_item_twice(self):
        """Add same menu item twice"""
        self.menu.add_category("Burgers")
        self.menu.add_menu_item("Burgers", "Cheeseburger", 20.00, "/cheeseburger.png")
        with self.assertRaises(expected_exception=ValueError):
            self.menu.add_menu_item("Burgers", "Cheeseburger", 20.00, "/cheeseburger.png")

    def test_remove_menu_item(self):
        """Remove menu item from existing category"""
        self.menu.add_category("Burgers")
        self.menu.add_menu_item("Burgers", "Cheeseburger", 20.00, "/cheeseburger.png")
        self.menu.remove_menu_item("Burgers", "Cheeseburger")
        self.assertIsNone(self.menu.get_menu_item("Burgers", "Cheeseburger"))

    def test_remove_menu_item_twice(self):
        """Remove same menu item twice"""
        self.menu.add_category("Burgers")
        self.menu.add_menu_item("Burgers", "Cheeseburger", 20.00, "/cheeseburger.png")
        self.menu.remove_menu_item("Burgers", "Cheeseburger")
        with self.assertRaises(expected_exception=ValueError):
            self.menu.remove_menu_item("Burgers", "Cheeseburger")

    def test_add_deal(self):
        """Add deal"""
        self.menu.add_category("Burgers")
        self.menu.add_menu_item("Burgers", "Cheeseburger", 20.00, "/cheeseburger.png")
        self.menu.add_menu_item("Burgers", "Quarter Pounder", 15.00, "/quarterpounder.png")
        self.menu.add_menu_item("Burgers", "Angus Burger", 17.00, "/angusburger.png")
        self.menu.add_deal(5.0, ["Cheeseburger", "Quarter Pounder"])
        self.assertIsInstance(self.menu.get_deals_by_id(0), Deal)

    def test_add_deal_nonexist(self):
        """Add deal with non-existing menu item"""
        self.menu.add_category("Burgers")
        self.menu.add_menu_item("Burgers", "Cheeseburger", 20.00, "/cheeseburger.png")
        self.menu.add_menu_item("Burgers", "Quarter Pounder", 15.00, "/quarterpounder.png")
        self.menu.add_menu_item("Burgers", "Angus Burger", 17.00, "/angusburger.png")
        with self.assertRaises(expected_exception=ValueError):
            self.menu.add_deal(5.0, ["Cheeseburger", "Random Burger"])

class UserTests(unittest.TestCase):
    """Tests for user handling functionality"""
    def setUp(self):
        self.app = Application()
        self.user = self.app.user_handler
        # self.user.add_user("John", "Doe", "Customer", "12345678")

    # def test_add_customer(self):
    #     self.user.
    def test_login_success(self):
        """Successful login"""
        self.user.add_user("John", "A", "Customer", "12345678")
        self.assertIsInstance(self.user.login("John", "A", "12345678"), Customer)

        self.user.add_user("John", "B", "KitchenStaff", "12345678")
        self.assertIsInstance(self.user.login("John", "B", "12345678"), KitchenStaff)

        self.user.add_user("John", "C", "WaitStaff", "12345678")
        self.assertIsInstance(self.user.login("John", "C", "12345678"), WaitStaff)

        self.user.add_user("John", "D", "Manager", "12345678")
        self.assertIsInstance(self.user.login("John", "D", "12345678"), Manager)
    
    def test_login_fail(self):
        """Failed login"""
        self.user.add_user("John", "A", "Customer", "12345678")
        self.assertIsNone(self.user.login("John", "A", "ABCDEFGH"))

        self.user.add_user("John", "B", "KitchenStaff", "12345678")
        self.assertIsNone(self.user.login("John", "B", "ABCDEFGH"))

        self.user.add_user("John", "C", "WaitStaff", "12345678")
        self.assertIsNone(self.user.login("John", "C", "ABCDEFGH"))

        self.user.add_user("John", "D", "Manager", "12345678")
        self.assertIsNone(self.user.login("John", "D", "ABCDEFGH"))



# class OrderTests(unittest.TestCase):
#     """Tests for order handling functionality"""

#     def setUp(self):
#         self.app = Application()
#         self.menu = self.app.menu_handler
#         self.table = self.app.table_handler
#         self.order = self.app.om_handler
#         self.menu.add_category("Burgers")
#         self.menu.add_menu_item("Burgers", "Cheeseburger", 20.00, "/cheeseburger.png")
#         self.menu.add_menu_item("Burgers", "Quarter Pounder", 15.00, "/quarterpounder.png")
#         self.menu.add_menu_item("Burgers", "Angus Burger", 17.00, "/angusburger.png")
#         self.menu.add_category("Pastas")
#         self.menu.add_menu_item("Pastas", "Sphagetti", 25.00, "/sphagetti.png")
#         self.menu.add_menu_item("Pastas", "Aglio Olio", 22.00, "/quarterpounder.png")
    
#     def test_add_order(self):
#         """Add new order"""
#         self.app.user_handler.add_user()
#         self.order.add_order()
#         self.table.add_table(4, )

if __name__ == '__main__':
    unittest.main()