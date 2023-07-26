import unittest
from wms import Application, Category, MenuItem, Deal, Order, Customer

class OrderTests(unittest.TestCase):
    """ Tests for menu handling functionality"""

    maxDiff = None

    def setUp(self):
        self.app = Application()
        self.menu = self.app.menu_handler
        self.table = self.app.table_handler
        self.order = self.app.om_handler
        self.menu.add_category("Burgers")
        self.menu.add_menu_item("Burgers", "Cheeseburger", 20.00, "/cheeseburger.png")      # menuId 0
        self.menu.add_menu_item("Burgers", "Quarter Pounder", 15.00, "/quarterpounder.png") # menuId 1
        self.menu.add_menu_item("Burgers", "Angus Burger", 17.00, "/angusburger.png")       # menuId 2
        self.menu.add_deal(5.0, ["Cheeseburger", "Angus Burger"])                           # dealId 0
        self.table.add_table(2, None)                                                       # tableId 0
        
    def test_add_tables(self):
        """Add another table, totalling two"""
        self.table.add_table(5, Order())
        self.assertEqual(len(self.table.tables), 2)

    def test_add_order_no_table(self):
        """Add order with wrong or non-existent table number"""
        # with self.assertRaisesRegex(ValueError, r'Table*'):
        with self.assertRaises(expected_exception=ValueError):
            self.order.add_order(10, [0, 1], [0])

    def test_add_order_no_menu(self):
        """Add order with wrong or non-existent menu item number"""
        # with self.assertRaisesRegex(ValueError, r'MenuItem*'):
        with self.assertRaises(expected_exception=ValueError):
            self.order.add_order(0, [5, 6], [0])

    def test_add_order_no_deal(self):
        """Add order with wrong or non-existent deal number"""
        # with self.assertRaisesRegex(ValueError, r'Deal*'):
        with self.assertRaises(expected_exception=ValueError):
            self.order.add_order(0, [0, 1], [9])

    def test_add_order_status(self):
        """Add order, check status"""
        self.order.add_order(0, [0, 1], [0])
        self.assertEqual(
            self.order.get_order_by_id(0).get("state"),
            "ordered"
        )

    def test_add_order_bill(self):
        """Add order, check bill"""
        self.order.add_order(0, [0, 1], [0])
        self.assertEqual(
            self.order.get_order_by_id(0).get("bill"),
            None
        )

    # def test_change_order_state(self):
    #     """Add order, change order state"""
    #     self.order.add_order(0, [2], [0])
    #     self.order.change_order_state(0)
    #     self.assertEqual(
    #         self.order.get_order_state(0),
    #         None
    #     )

    # def test_change_menu_item_state(self):

    # def test_remove_order(self):

    # def test_remove_order_by_id(self):

    # def test_calculate_bill(self):


            

