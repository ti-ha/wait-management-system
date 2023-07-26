import unittest
from wms import Application, Category, MenuItem, Deal

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