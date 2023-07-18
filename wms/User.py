from __future__ import annotations
import itertools
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self, firstname, lastname, password):
        """ Constructor for the User Class

        Args:
            firstname (string): First Name of the User
            lastname (string): Last Name of the User
        """
        self.__id = next(User.__id_iter)
        self.__firstname = firstname
        self.__lastname = lastname
        self.__password = generate_password_hash(password)

    # Getters
    @property
    def firstname(self) -> str:
        """ Returns user's first name """
        return self.__firstname

    @property
    def lastname(self) -> str:
        """ Returns user's last name """
        return self.__lastname
    
    @property
    def id(self) -> itertools.count:
        """ Returns user's ID """
        return self.__id
    
    @property
    def password_hash(self) -> str:
        return self.__password
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def jsonify(self):
        return {"id": self.id,
                "first_name": self.firstname,
                "last_name": self.lastname,
                "usertype": self.__class__.__name__,
                "password": self.password_hash}

