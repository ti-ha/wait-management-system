from __future__ import annotations
import itertools

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
        self.__password = None

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
    def password_hash(self) -> None:
        return None
    
    @property
    def password(self):
        return self.__password
    
    def check_password(self, password):
        return self.password_hash
    
    def jsonify(self):
        return {"id": self.id,
                "first_name": self.firstname,
                "last_name": self.lastname,
                "usertype": self.__class__.__name__}

