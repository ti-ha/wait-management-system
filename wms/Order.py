import itertools

class Order:

    # Unique identifier starting from 0
    __id_iter = itertools.count()
    
    def __init__(self, menu_items=None, deals=None):
        self.__id = next(Order.__id_iter)
        self.__menu_items = menu_items
        self.__deals = deals

        # Initialize empty lists
        if self.__menu_items == None:
            self.__menu_items = []

        if self.__deals == None:
            self.__deals == []
        #self.__status: State (NOT YET IMPLEMENTED)