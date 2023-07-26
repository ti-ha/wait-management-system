import unittest
from wms import Application, Category, MenuItem, Deal, Order, Customer

class OrderTests(unittest.TestCase):
    """ Tests for menu handling functionality"""

    def setUp(self):
        self.app = Application()
        self.menu = self.app.menu_handler
        self.table = self.app.table_handler
        self.table.add_table(5, Order())    # id 1
        self.table.add_table(4, Order())    # id 2
        self.table.add_table(3, Order())    # id 3

    def test_add_tables(self):
        """Add three tables"""
        self.table.add_table(5, Order())
        self.table.add_table(4, Order())
        self.table.add_table(3, Order())
        self.assertEqual(len(self.table.tables), 6)

    def test_add_customer(self):
        """Add customer to table"""
        self.table.add_customer(0, Customer("Guest", "1", "123"))
        self.table.add_customer(0, Customer("Guest", "2", "123"))
        self.table.add_customer(0, Customer("Guest", "3", "123"))
        

