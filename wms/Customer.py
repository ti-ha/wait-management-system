import User

class Customer(User):
    def __init__(self, firstname, lastname):
        super().__init__(self, firstname, lastname)

    def __init__(self, firstname, lastname, table):
        super().__init__(self, firstname, lastname)
        self.__table = table
    
    # Getters and Setters
    def get_table(self):
        return self.__table
    
    def set_table(self, table):
        self.__table = table