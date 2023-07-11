from __future__ import annotations
from .User import User
from wms import Order
from werkzeug.security import generate_password_hash, check_password_hash

class KitchenStaff(User):
    def __init__(self, firstname, lastname, password):
        """ Constructor of the KitchenStaff class that inherits the User Class

        Args:
            firstname (string): First Name of the User
            lastname (string): Last Name of the User
            password (string): Password of the user
        """
        super().__init__(firstname, lastname, password)
        self.__password = generate_password_hash(password)
        self.__orders = []

    @property
    def orders(self) -> list[Order]:
        """ Gets the kitchen staff order list """
        return self.__orders
    
    @property
    def password_hash(self):
        return self.__password
    
    def check_password(self, password):
        return check_password_hash(self.__password, password)

    def assign_order(self, order: Order):
        """ Add to list of orders

        Args:
            order (Order): Order to be assigned to the kitchen staff

        Raises:
            TypeError: Raised when order argument is not of type Order
            ValueError: Raised when order already exists in the list of assigned 
            orders
        """
        if not isinstance(order, Order):
            raise TypeError("KitchenStaff: assign_order(): Object is not of type Order")
        
        if order in self.__orders:
            raise ValueError("KitchenStaff: assign_order(): Order already exists")
        self.__orders.append(order)

    def remove_order(self, order: Order):
        """ Remove order from the list of orders

        Args:
            order (Order): Order to be removed from the list of orders

        Raises:
            TypeError: Raised when order argument is not of type Order
            ValueError: Raised when order does not exist in the list of assigned 
            orders
        """
        if not isinstance(order, Order):
            raise TypeError("KitchenStaff: remove_order(): Object is not of type Order")
        
        if order not in self.__orders:
            raise ValueError("KitchenStaff: remove_order(): Order does not exist")
        orderNum = self.__orders.index(order)
        self.orders[orderNum].change_state()
        # Move order to wait staff
        self.__orders.remove(order) 