from .User import User

class Customer(User):
    def __init__(self, firstname="Guest", lastname="Customer", table=None):
        super().__init__(firstname, lastname)
        self.__table = table
        if table is not None:
            self.__table.add_customers(self)
    
    # Getters and Setters
    def get_table(self):
        return self.__table
    
    def set_table(self, table):
        self.__table = table
        self.__table.add_customers(self)