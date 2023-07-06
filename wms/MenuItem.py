import itertools

class MenuItem():

    # Unique id
    __id_iter = itertools.count()

    def __init__(self, name, price, image_url = "None"):
        """ Constructor for the MenuItem class

        Args:
            name (string): Name of the menu item
            price (float): Price of the menu item
            image_url (str, optional): URL of an image of the menu item. 
            Defaults to "None".
        """
        self.__id = next(MenuItem.__id_iter)
        self.__name = name
        self.__price = price
        self.__image_url = image_url

    @property
    def id(self) -> itertools.count:
        """ Returns menu item ID """
        return self.__id

    @property
    def name(self) -> str:
        """ Returns menu item name """
        return self.__name
    
    @name.setter
    def name(self, name):
        """ Sets the menu item name """
        if not isinstance(name, str):
            raise TypeError("MenuItem: menu_item.set_name(name): argument is not string")
        self.__name = name
    
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
        
    def jsonify(self):
        """ Creates a dictionary containing the id, name, price and image URL  
        of the menu item 

        Returns:
            dict: Dictionary containing the id, name, price and image URL  
        of the menu item 
        """
        return {"id": self.id, "name": self.name, "price": self.price, "imageURL": self.image_url}
