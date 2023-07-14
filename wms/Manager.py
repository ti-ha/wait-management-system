from .User import User
from werkzeug.security import generate_password_hash, check_password_hash

# Has no other attributes differentiating itself from a user
# only important difference is type. Also can see OrderManager
class Manager(User):
    def __init__(self, firstname, lastname, password):
        """ Constructor of the Manager class that inherits the User Class

        Args:
            firstname (string): First Name of the User
            lastname (string): Last Name of the User
            password (string): Password of the user
        """
        super().__init__(firstname, lastname, password)
        self.__password = generate_password_hash(password)

    @property
    def password_hash(self):
        return self.__password
        
    def check_password(self, password):
        return check_password_hash(self.__password, password)