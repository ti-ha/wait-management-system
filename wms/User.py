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
    def get_firstname(self) -> str:
        return self.__firstname

    def get_lastname(self) -> str:
        return self.__lastname
    
    def get_id(self) -> itertools.count:
        return self.__id