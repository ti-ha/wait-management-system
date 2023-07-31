import itertools
# from sqlalchemy import Column, Integer, Double, String, ForeignKey

class MenuItem():

    # Unique id
    __id_iter = itertools.count()

    # __tablename__ = 'menu_item'

    # # _id = Column(Integer, primary_key=True, autoincrement='auto')
    # # _name = Column(String(40), nullable=False)
    # # _price = Column(Double(2), nullable=False)
    # # _category = Column(Integer, ForeignKey('category.categoryId'))
    # # _image_url = Column(String(256))

    def __init__(self, name, price, image_url = "None"):
        """ Constructor for the MenuItem class

        Args:
            name (String): Name of the menu item
            price (Float): Price of the menu item
            image_url (String, optional): URL of an image of the menu item. 
            Defaults to "None".
        """

        self.__id = next(MenuItem.__id_iter)
        self.__name = name
        self.__price = price
        self.__image_url = image_url
        self.__visible = True
        # self.__db_engine = db_engine

    @property
    def id(self) -> itertools.count:
        """ Returns menu item ID """
        return self.__id

    @property
    def name(self) -> str:
        """ Returns menu item name """
        return self.__name
    
    #TODO add UPDATE statements in all setters to update database
    @name.setter
    def name(self, name):
        """ Sets the menu item name """
        if not isinstance(name, str):
            raise TypeError("MenuItem: menu_item.set_name(name): argument is not string")
        self.__name = name
        # stmt = (
        #     update(menu_item).
        #     where(menu_item.c._id == self.id).
        #     values(_name = self.name)
        # )
    
    @property
    def price(self) -> float:
        """ Returns menu item price """
        return self.__price
    
    @price.setter
    def price(self, price):
        """ Sets the menu item price """
        if not isinstance(price, float):
            raise TypeError("MenuItem: menu_item.set_price(price): argument is not floatable")
        self.__price = price
    
    @property
    def image_url(self) -> str: 
        """ Returns menu item image url """
        return self.__image_url

    @image_url.setter
    def image_url(self, image_url: str):
        """ Sets the menu item image url """
        self.__image_url = image_url

    @property
    def visible(self) -> bool: 
        """ Returns menu item visibility """
        return self.__visible

    @visible.setter
    def visible(self, visible):
        """ Sets the menu item visibility """
        self.__visible = visible
    
    def is_equal(self, menu_item):
        """ Checks if another menu_item is equal to this one

        Args:
            menu_item (MenuItem): Menu item to be compared to this current one
        """
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
        
    def update(self, name, price, image_url, visible):
        """ Updates menu item with new name, price or image_url

        Args:
            name (String): Name of the menu item
            price (String): Price of the menu item
            image_url (String): URL of an image of the menu item.
            visible (String): Visibility of the menu item
        """
        if name is not None: self.name = name 
        if price is not None: self.price = float(price) 
        if image_url is not None: self.image_url = image_url 
        if visible is not None: self.visible = (visible == "True")

    def jsonify(self):
        """ Creates a dictionary containing the id, name, price and image URL  
        of the menu item 

        Returns:
            dict: Dictionary containing the id, name, price and image URL  
        of the menu item 
        """
        return {"id": self.id, "name": self.name, "price": self.price, 
                "imageURL": self.image_url, "visible": self.visible}
