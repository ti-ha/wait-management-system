import itertools
from Order import Order
from Customer import Customer

class Table:

    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self, tablelimit, orders=[]):
        self.__id = next(Table.__id_iter)
        self.__orders = orders
        self.__customers = []
        self.__occupied = False
        self.__tablelimit = tablelimit

    # Getters
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

    # Adding to the list of customers/orders
    def add_customers(self, customer):
        if not isinstance(customer, Customer):
            raise TypeError("Table: add_customers(): Object is not of type Customer")
        self.__customers.append(customer)
        if len(self.__customers) >= self.__tablelimit:
            self.__occupied = True

    def add_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("Table: add_order(): Object is not of type Order")
        self.__orders.append(order)

    # Getting the current/final bill for the table
    def request_bill(self):
        return; 