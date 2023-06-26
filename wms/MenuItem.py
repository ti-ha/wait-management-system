import itertools
from .Application import Base
from sqlalchemy import Column, Integer, Double, String, ForeignKey

class MenuItem(Base):

    # Unique id
    __id_iter = itertools.count()
    
    __tablename__ = 'menu_item'
    itemId = Column(Integer, primary_key=True)
    itemName = Column(String(40), nullable=False)
    itemPrice = Column(Double(2), nullable=False)
    itemCategory = Column(Integer, ForeignKey('category.categoryId'))

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
        
    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False
        
    def jsonify(self):
        return {"id": self.id(), "name": self.name(), "price": self.price(), "imageURL": self.imageURL()}
