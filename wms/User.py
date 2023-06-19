import itertools

class User:
    # Unique identifier starting from 0
    __id_iter = itertools.count()

    # Constructor for non-logged in user
    def __init__(self):
        self.__id = next(User.__id_iter)

    # Constructor for logged in user
    def __init__(self, firstname, lastname):
        self.__id = next(User.__id_iter)
        self.__firstname = firstname
        self.__lastname = lastname

    # Getters
    def get_firstname():
        return self.__firstname

    def get_lastname():
        return self.__lastname