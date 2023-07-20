from __future__ import annotations
import itertools
from .Order import Order
from .Customer import Customer
from .Bill import Bill

class Table:

    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self, table_limit, orders=None):
        """ Constructor for Table class

        Args:
            table_limit (integer): Limit to how many people can be seated at
            this table
            orders (List[Order], optional): List of orders to be predefined 
            with the table. Defaults to None.
        """
        self.__id = next(Table.__id_iter)
        # Initialize empty list
        self.__orders = [] if orders is None else orders
        self.__customers = []
        self.__occupied = False
        self.__table_limit = table_limit
        self.__bill = None

    # Getters for the class variables
    @property
    def id(self) -> itertools.count:
        """ Returns table ID """
        return self.__id

    @property
    def occupied(self) -> bool:
        """ Returns if the table is occupied """
        return self.__occupied
    
    @property
    def orders(self) -> list[Order]:
        """ Returns list of orders for the table """
        return self.__orders

    @property
    def customers(self) -> list[Customer]:
        """ Returns list of customers at the table """
        return self.__customers
    
    @property
    def table_limit(self) -> int:
        """ Returns the table person limit """
        return self.__table_limit
    
    @property
    def bill(self) -> Bill:
        """ Returns the table bill """
        return self.__bill
    
    # Setter for the bill 
    @bill.setter
    def bill(self, bill: Bill):
        """ Sets the table bill """
        self.__bill = bill

    def get_open_seats(self) -> str:
        """ Unique getter to show how many open seats there are

        Returns:
            String: String that describes the number of open seats out of the 
            total number of seats or the string FULL if there are no open seats
        """
        open_seats = self.__table_limit - len(self.__customers)
        return f"{open_seats} / {self.__table_limit}" if open_seats != 0 else "FULL"

    def add_customers(self, customer):
        """Adding a customer to the list of customers

        Args:
            customer (Customer): Customer to be added to the table

        Raises:
            TypeError: Raised when customer argument is not of type Customer
            ValueError: Raised when either the Customer already exists or the 
            table is full
        """
        if not isinstance(customer, Customer):
            raise TypeError("Table: add_customers(): Object is not of type Customer")
        
        if customer in self.__customers:
            raise ValueError("Table: add_customers(): Customer already exists")
        
        if self.__occupied:
            raise ValueError("Table: add_customers(): Table is full")
        
        self.__customers.append(customer)
        customer.table = self
        if len(self.__customers) >= self.__table_limit:
            self.__occupied = True

    def add_order(self, order):
        """ Adding an order to the list of orders

        Args:
            order (Order): Order to be added to the table

        Raises:
            TypeError: Raised when order argument is not of type Order
            ValueError: Raised when the Order already exists
        """
        if not isinstance(order, Order):
            raise TypeError("Table: add_order(): Object is not of type Order")
        
        if order in self.__orders:
            raise ValueError("Table: add_order(): Order already exists")
        
        self.__orders.append(order)

    def remove_order(self, order):
        """ Removing an order from the list of orders

        Args:
            order (Order): Order to be removed from the table

        Raises:
            TypeError: Raised when order argument is not of type Order
            ValueError: Raised when the Order does not exist
        """
        if not isinstance(order, Order):
            raise TypeError("Table: remove_order(): Object is not of type Order")
        
        if order not in self.__orders:
            raise ValueError("Table: remove_order(): Order does not exist")
        
        self.__orders.remove(order)

    def jsonify(self):
        return {
            "id": self.id,
            "availability": self.get_open_seats(),
            "table_limit": self.table_limit,
            "is_occupied": self.occupied
        }