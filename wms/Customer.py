from User import User

class Customer(User):
    def __init__(self, firstname="Guest", lastname="Customer"):
        super().__init__(firstname, lastname)
        self.__table = None
    
    # Getters and Setters
    def get_table(self):
        return self.__table
    
    def set_table(self, table):
        self.__table = table