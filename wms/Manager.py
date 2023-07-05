from .User import User

# Has no other attributes differentiating itself from a user
# only important difference is type. Also can see OrderManager
class Manager(User):
    def __init__(self, firstname, lastname):
        """ Constructor of the Manager class that inherits the User Class

        Args:
            firstname (string): First Name of the User
            lastname (string): Last Name of the User
        """
        super().__init__(firstname, lastname)
        pass