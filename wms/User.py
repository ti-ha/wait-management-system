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
        self.__logged_in = False

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
        """ Returns user's hashed password """
        return self.__password
    
    @property
    def status(self) -> bool:
        """ Returns user's logged in status """
        return self.__logged_in
    
    @status.setter
    def status(self, status: bool):
        """ Sets the user's logged in status """
        self.__logged_in = status
    
    def check_password(self, password) -> bool:
        """ Check given password against hashed password """
        return check_password_hash(self.password_hash, password)
    
    def jsonify(self) -> dict:
        """ Creates a dictionary containing the id, first name, last name, 
        usertype and password of all the users.

        Returns:
            Dict: Creates a dictionary containing the id, first name, last name, 
        usertype and password of all the users.
        """
        return {"id": self.id,
                "first_name": self.firstname,
                "last_name": self.lastname,
                "usertype": self.__class__.__name__,
                "password": self.password_hash}

