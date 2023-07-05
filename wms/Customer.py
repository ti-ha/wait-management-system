from .User import User

class Customer(User):
    def __init__(self, firstname="Guest", lastname="Customer"):
        """ Constructor of the Customer class that inherits the User Class
        Args:
            firstname (str, optional): First Name of the User. Defaults to 
            "Guest".
            lastname (str, optional): Last Name of the User. Defaults to 
            "Customer".
        """
        super().__init__(firstname, lastname)
        self.__table = None
    
    # Getters and Setters
    def get_table(self):
        return self.__table
    
    def set_table(self, table):
        self.__table = table