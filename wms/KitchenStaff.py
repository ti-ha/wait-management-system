from .User import User

class KitchenStaff(User):
    def __init__(self, firstname: str, lastname: str, password: str):
        """ Constructor of the KitchenStaff class that inherits the User Class

        Args:
            firstname (str): First Name of the User
            lastname (str): Last Name of the User
            password (str): Password of the user
        """
        super().__init__(firstname, lastname, password)