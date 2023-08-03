import unittest
from wms import Application, Customer, WaitStaff, KitchenStaff, Manager

class UserTests(unittest.TestCase):
    """Tests for user handling functionality"""

    def setUp(self):
        self.app = Application()
        self.user = self.app.user_handler

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

    def test_login_fail_password(self):
        """Failed login with wrong password"""
        self.user.add_user("John", "A", "Customer", "12345678")
        self.assertIsNone(self.user.login("John", "A", "ABCDEFGH"))

        self.user.add_user("John", "B", "KitchenStaff", "12345678")
        self.assertIsNone(self.user.login("John", "B", "ABCDEFGH"))

        self.user.add_user("John", "C", "WaitStaff", "12345678")
        self.assertIsNone(self.user.login("John", "C", "ABCDEFGH"))

        self.user.add_user("John", "D", "Manager", "12345678")
        self.assertIsNone(self.user.login("John", "D", "ABCDEFGH"))

    def test_login_fail_name(self):
        """Failed login with wrong names"""
        self.user.add_user("John", "A", "Customer", "12345678")
        self.assertIsNone(self.user.login("Tom", "A", "12345678"))

        self.user.add_user("John", "B", "KitchenStaff", "12345678")
        self.assertIsNone(self.user.login("Tom", "B", "12345678"))

        self.user.add_user("John", "C", "WaitStaff", "12345678")
        self.assertIsNone(self.user.login("Tom", "C", "12345678"))

        self.user.add_user("John", "D", "Manager", "12345678")
        self.assertIsNone(self.user.login("Tom", "D", "12345678"))
