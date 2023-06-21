from User import User
from Table import Table

class Customer(User):
    def __init__(self, firstname="Guest", lastname="Customer", table=None):
        super().__init__(firstname, lastname)
        if not isinstance(table, Table):
            raise TypeError("Customer: constructor(): Object is not of type Table")
        self.__table = table
        if table is not None:
            self.__table.add_customers(self)
    
    # Getters and Setters
    def get_table(self):
        return self.__table
    
    def set_table(self, table):
        if not isinstance(table, Table):
            raise TypeError("Customer: set_table(): Object is not of type Table")
        self.__table = table
        self.__table.add_customers(self)