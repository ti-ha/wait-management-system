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
        super().__init__(firstname, lastname, None)
        self.__table = None
    
    @property
    def table(self):
        """ Returns table the customer is at """
        return self.__table
    
    @table.setter   
    def table(self, table) -> None:
        """ Sets the table the customer will be at """
        self.__table = table