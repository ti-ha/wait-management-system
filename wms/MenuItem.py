import itertools

class MenuItem():

    # Unique id
    __id_iter = itertools.count()

    def __init__(self, name, price, imageURL="None"):
        self.__id = next(MenuItem.__id_iter)
        self.__name = name
        self.__price = price
        self.__imageURL = imageURL

    def id(self):
        return self.__id
    
    def name(self):
        return self.__name
    
    def price(self):
        return self.__price
    
    def imageURL(self): 
        return self.__imageURL
    
    def get_name(self):
        return self.__name

    def set_name(self, name):
        if not isinstance(name, str):
            raise TypeError("MenuItem: menu_item.set_name(name): argument is not string")
        
        self.__name = name
    
    def set_price(self, price):
        if not MenuItem.isfloat(price):
            raise TypeError("MenuItem: menu_item.set_price(price): argument is not floatable")

        self.__price = price

    def set_image_url(self, imageurl: str):
        self.__imageURL = imageurl
    
    def is_equal(self, menu_item):
        if isinstance(menu_item, MenuItem):
            if self.__name == menu_item.get_name():
                return True
            else: 
                return False
        else:
            return False
        
    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False
        
    def jsonify(self):
        return {"id": self.id(), "name": self.name(), "price": self.price(), "imageURL": self.imageURL()}
