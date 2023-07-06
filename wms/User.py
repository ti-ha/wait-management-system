from __future__ import annotations
import itertools

class User:
    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self, firstname, lastname):
        """ Constructor for the User Class

        Args:
            firstname (string): First Name of the User
            lastname (string): Last Name of the User
        """
        self.__id = next(User.__id_iter)
        self.__firstname = firstname
        self.__lastname = lastname

    # Getters
    @property
    def firstname(self) -> str:
        """ Returns user's first name """
        return self.__firstname

    @property
    def get_lastname(self) -> str:
        """ Returns user's last name """
        return self.__lastname
    
    @property
    def id(self) -> itertools.count:
        """ Returns user's ID """
        return self.__id