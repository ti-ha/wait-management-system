import itertools
import Order
import Customer

class Table:

    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self):
        self.__id = next(Table.__id_iter)
        self.__orders = []
        self.__customers = []
        self.__occupied = False
    
    def __init__(self, orders):
        self.__id = next(Table.__id_iter)
        self.__orders = orders
        self.__customers = []
        self.__occupied = False

    # Getters
    def is_occupied(self):
        return self.__occupied
    
    def get_orders(self):
        return self.__orders
    
    def get_order(self, orderNumber):
        return self.__orders[orderNumber]

    def get_customers(self):
        return self.__customers

    # Adding to the list of customers/orders
    def add_customers(self, customer):
        self.__customers.append(customer)

    def add_order(self, order):
        self.__orders.append(order)

    # Getting the current/final bill for the table
    def request_bill(self):
        return; 