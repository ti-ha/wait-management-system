import itertools

class MenuItem():

    # Unique id
    __id_iter = itertools.count()

    def __init__(self, name, price):
        self.__id = next(MenuItem.__id_iter)
        self.__name = name
        self.__price = price

    def id(self):
        return self.__id
    
    def name(self):
        return self.__name
    
    def price(self):
        return self.__price
    
    def set_name(self, name):
        if not isinstance(name, str):
            raise TypeError("MenuItem: menu_item.set_name(name): argument is not string")
        
        self.__name = name
    
    def set_price(self, price):
        if not MenuItem.isfloat(price):
            raise TypeError("MenuItem: menu_item.set_price(price): argument is not floatable")

        self.__price = price
        
    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False
