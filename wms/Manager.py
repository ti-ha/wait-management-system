from .User import User

# Has no other attributes differentiating itself from a user
# only important difference is type.
class Manager(User):
    def __init__(self, firstname: str, lastname: str, password: str, 
                 password_hash: str = None)):
        """ Constructor of the Manager class that inherits the User Class

        Args:
            firstname (str): First Name of the User
            lastname (str): Last Name of the User
            password (str): Password of the user
            password_hash (str, optional): Existing hashed password. Defaults to
            None.
        """
        super().__init__(firstname, lastname, password, password_hash)