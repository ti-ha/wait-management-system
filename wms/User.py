import itertools

class User:
    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self, firstname, lastname):
        self.__id = next(User.__id_iter)
        self.__firstname = firstname
        self.__lastname = lastname
        