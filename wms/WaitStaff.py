from __future__ import annotations
from wms import User, ServiceRequest

class WaitStaff(User):
    def __init__(self, firstname, lastname, password):
        """ Constructor of the WaitStaff class that inherits the User Class

        Args:
            firstname (string): First Name of the User
            lastname (string): Last Name of the User
            password (string): Password of the user
        """
        super().__init__(firstname, lastname, password)
    