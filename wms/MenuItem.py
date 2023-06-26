import itertools
from .Application import Base
from sqlalchemy import Column, Integer, Double, String, ForeignKey

class MenuItem(Base):

    # Unique id
    __id_iter = itertools.count()

    __tablename__ = 'menu_item'

    _id = Column(Integer, primary_key=True, autoincrement='auto')
    _name = Column(String(40), nullable=False)
    _price = Column(Double(2), nullable=False)
    _category = Column(Integer, ForeignKey('category.categoryId'))
    _image_url = Column(String(256))

    def __init__(self, name, price, image_url = None):
        self.id = next(MenuItem.__id_iter)
        self._name = name
        self._price = price
        self._image_url = image_url

    def id(self):
        return self.id
    
    def name(self):
        return self._name
    
    def price(self):
        return self._price
    
    def image_url(self): 
        return self._image_url
    
    def set_name(self, name):
        if not isinstance(name, str):
            raise TypeError("MenuItem: menu_item.set_name(name): argument is not string")
        
        self.__name = name
    
    def set_price(self, price):
        if not MenuItem.isfloat(price):
            raise TypeError("MenuItem: menu_item.set_price(price): argument is not floatable")

        self.__price = price

    def set_image_url(self, image_url: str):
        self.__image_url = image_url
        
    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False
        
    def jsonify(self):
        return {"id": self.id(), "name": self.name(), "price": self.price(), "image_url": self.image_url()}
