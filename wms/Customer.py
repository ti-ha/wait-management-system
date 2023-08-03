from .User import User

class Customer(User):
    def __init__(self, firstname: str = "Guest", lastname: str = "Customer", 
                 password: str = "1234", password_hash: str = None):
        """ Constructor of the Customer class that inherits the User Class
        Args:
            firstname (str, optional): First Name of the User. Defaults to 
            "Guest".
            lastname (str, optional): Last Name of the User. Defaults to 
            "Customer".
            password (str, optional): Password of the User. Defaults to "1234".
            password_hash (str, optional): Existing hashed password. Defaults to
            None.
        """
        super().__init__(firstname, lastname, password, password_hash)
        self.__table = None
    
    @property
    def table(self):
        """ Returns table the customer is at """
        return self.__table
    
    @table.setter   
    def table(self, table):
        """ Sets the table the customer will be at """
        self.__table = table