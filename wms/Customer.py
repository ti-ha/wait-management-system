from .User import User
from werkzeug.security import generate_password_hash, check_password_hash

class Customer(User):
    def __init__(self, firstname="Guest", lastname="Customer", password=None):
        """ Constructor of the Customer class that inherits the User Class
        Args:
            firstname (str, optional): First Name of the User. Defaults to 
            "Guest".
            lastname (str, optional): Last Name of the User. Defaults to 
            "Customer".
        """
        super().__init__(firstname, lastname, password)
        self.__table = None
        self.__password = generate_password_hash(password)
    
    @property
    def table(self):
        """ Returns table the customer is at """
        return self.__table
    
    @property
    def password_hash(self):
        return self.__password
    
    @table.setter   
    def table(self, table) -> None:
        """ Sets the table the customer will be at """
        self.__table = table

    def check_password(self, password):
        return check_password_hash(self.__password, password)