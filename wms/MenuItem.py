import itertools

class MenuItem():

    # Unique id
    __id_iter = itertools.count()

    def __init__(self, name, price, image_url = "None"):
        self.__id = next(MenuItem.__id_iter)
        self.__name = name
        self.__price = price
        self.__image_url = image_url

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("MenuItem: menu_item.set_name(name): argument is not string")
        self.__name = name
    
    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, price):
        if not isinstance(price, float):
            raise TypeError("MenuItem: menu_item.set_price(price): argument is not floatable")
        self.__price = price
    
    @property
    def image_url(self): 
        return self.__image_url

    @image_url.setter
    def image_url(self, image_url: str):
        self.__image_url = image_url
    
    def is_equal(self, menu_item):
        bool(isinstance(menu_item, MenuItem) and self.name == menu_item.name)
        
        #     if self.__name == menu_item.name:
        #         return True
        #     else: 
        #         return False
        # else:
        #     return False
        
    # def is_float(self, num):
    #     try:
    #         float(num)
    #         return True
    #     except ValueError:
    #         return False
        
    def jsonify(self):
        return {"id": self.id, "name": self.name, "price": self.price, "imageURL": self.image_url}
