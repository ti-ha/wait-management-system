import itertools
from .Order import Order

class Table:

    # Unique identifier starting from 0
    __id_iter = itertools.count()

    def __init__(self):
        self.__id = next(Table.__id_iter)
        self.__orders = []
        self.__occupied = False
    
    def __init__(self, orders):
        self.__id = next(Table.__id_iter)
        self.__orders = orders
        self.__occupied = False




