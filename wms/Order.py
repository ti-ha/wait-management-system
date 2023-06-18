import itertools

class Order:

    # Unique identifier starting from 0
    __id_iter = itertools.count()
    
    def __init__(self):
        self.__id = next(Order.__id_iter)
        self.__menu_items = []
        self.__deals = []
        #self.__status: State (NOT YET IMPLEMENTED)
    
    def __init__(self, menu_items):
        self.__id: next(Order.__id_iter)
        self.__menu_items =  menu_items
        self.__deals = []

    def __init__(self, menu_items, deals):
        self.__id = next(Order.__id_iter)
        self.__menu_items = menu_items
        self.__deals = deals