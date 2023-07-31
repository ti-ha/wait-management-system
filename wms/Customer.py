from .User import User

class Customer(User):
    def __init__(self, firstname="Guest", lastname="Customer", password="1234"):
        """ Constructor of the Customer class that inherits the User Class
        Args:
            firstname (str, optional): First Name of the User. Defaults to 
            "Guest".
            lastname (str, optional): Last Name of the User. Defaults to 
            "Customer".
            password (str, optional): Password of the User. Defaults to "1234".
        """
        super().__init__(firstname, lastname, password)
        self.__table = None
    
    @property
    def table(self):
        """ Returns table the customer is at """
        return self.__table
    
    @table.setter   
    def table(self, table) -> None:
        """ Sets the table the customer will be at """
        self.__table = table