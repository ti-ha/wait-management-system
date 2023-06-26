import itertools
from .Order import Order
from .Customer import Customer
from .Application import Base
from sqlalchemy import Column, Integer, Double, String, ForeignKey
class Table:

    # Unique identifier starting from 0
    __id_iter = itertools.count()
    __tablename__ = 'table'
    tableId = Column(Integer, primary_key=True)
    occupied = Column(bool)
    
    # Constructor for Table class
    def __init__(self, tablelimit, orders=None):
        self.__id = next(Table.__id_iter)
        # Initialize empty list
        self.__orders = [] if orders == None else orders
        self.__customers = []
        self.__occupied = False
        self.__tablelimit = tablelimit

    # Getters
    def get_id(self):
        return self.__id

    def is_occupied(self):
        return self.__occupied
    
    def get_orders(self):
        return self.__orders
    
    def get_order(self, orderNumber):
        return self.__orders[orderNumber]

    def get_customers(self):
        return self.__customers
    
    def get_tablelimit(self):
        return self.__tablelimit

    # Unique getter to show how many open seats there are
    def get_open_seats(self):
        open_seats = self.__tablelimit - len(self.__customers)
        return str(open_seats) + " / " + str(self.__tablelimit) if open_seats != 0 else "FULL"

    # Adding a custoemr to the list of customers
    def add_customers(self, customer):
        if not isinstance(customer, Customer):
            raise TypeError("Table: add_customers(): Object is not of type Customer")
        
        if customer in self.__customers:
            raise ValueError("Table: add_customers(): Customer already exists")
        
        if self.__occupied:
            raise ValueError("Table: add_customers(): Table is full")
        
        self.__customers.append(customer)
        customer.set_table(self)
        if len(self.__customers) >= self.__tablelimit:
            self.__occupied = True

    # Adding an order to the list of orders
    def add_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("Table: add_order(): Object is not of type Order")
        
        if order in self.__orders:
            raise ValueError("Table: add_order(): Order already exists")
        
        self.__orders.append(order)

    # Getting the current bill for the table
    def request_bill(self):
        curr_bill = 0
        for order in self.__orders:
            if not isinstance(order, Order):
                raise TypeError("Table: request_bill(): Object is not of type Order")
            curr_bill += order.calculate_bill().get_price()
        return curr_bill 